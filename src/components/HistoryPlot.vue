<template>
  <div class="card" style="margin-bottom: 5px" :style="{'height': `calc(${divHeight}vh)`}">
    <div class="card-body" style="padding: 0px 15px 0px 20px">
      <div style="float: right">
        <button
          v-if="asset_curve_zoom_recent"
          id="btn_zoom_reset"
          @click="onClickBtnZoomSet(1)"
          class="widget-button"
        >
          <!-- <font-awesome-icon
            icon="fa-solid fa-magnifying-glass"
            class="text-info"
          /> -->
          Show History
        </button>
        <button
          v-else
          id="btn_zoom_latest"
          @click="onClickBtnZoomSet(0)"
          class="widget-button"
        >
          <!-- <font-awesome-icon
            icon="fa-solid fa-magnifying-glass-plus"
            class="text-info"
          /> -->
          Show Recent
        </button>
      </div>
      <div id="div_history" style="height:100%"></div>
    </div>
  </div>
</template>
<script>
import * as d3 from "d3v4";
import { gvars } from "../gvars";
import { bus } from "../main";
import $ from "jquery";

export default {
  props: {
    plotName: {
      // show as the left axis
      type: String,
      default: "default_name",
    },
    plotData: {
      // default place holder for plotData
      type: Object,
      default: () => {
        return null;
      },
    },
    curAsset: {
      type: String,
      default: "bitcoin",
    },
    divHeight: {
      type: Number,
      default: 30
    },
    yLeftField: {
      // the field of the left axis
      type: Object,
      default: null,
    },
    yRightField: {
      // the field of the right axis, and show the name
      type: Object,
      default: null,
    },
    shareLeftField: {
      type: Boolean,
      default: false,
    },
    zoomRedDot: {
      type: Boolean,
      default: true,
    },
    cursorLabel: { // show cursor label or not
      type: Boolean,
      default: true,
    },
    primaryAxis: {
      type: String,
      default: 'Left'
    }
  },
  computed: {},
  watch: {
    plotName: function (newVal, oldVal) {
      let vm = this;
      vm.drawAxisName()
    },
    plotData: {
      deep: true, // Enable deep watching
      handler(newVal, oldVal) {
        let vm = this;
        if (!vm.initialized) {
          vm.initChart();
        }

        vm.updateXGAxisScale();

        // set the current zoom range to local range and call drawChart()
        vm.onClickBtnZoomSet(0);

        // vm.drawChart();  
      },
    },
  },
  data() {
    return {
      asset_curve_zoom_recent: 0,
      width: 0,
      height: 0,
      contentWidth: 0,
      contentHeight: 0,
      margin: { left: 70, right: 40, top: 10, bottom: 30 },
      uiHeight: 30,              //zoom UI button height
      svg: null,

      xMarginRatio: 0.00001,
      yMarginRatio: 0.005,

      xScale: null,
      yScale: null,
      xGScale: null,

      disableEventDispatch: 0,

      xCursorLabelWidth: gvars.newsTimeScaleUTC? 168:130,  // the width of the x label for cursor position, showing date
      xCursorLabelHeight: 20,  // the height of the x label for cursor rectangle, showing date
      yCursorLabelWidth: 60,   // the width of the y label for cursor rectangle (y value)
      yCursorLabelHeight: 20,  // the height of the y label for cursor rectangle

      highlightMatchedCurveMame: "",
      visPartData: [],      // the visible part of the curve
      initialized: false,     // whether the view has been initialized or not
    };
  },
  methods: {
    /**
     * this is called when there is no data yet
     * append SVG, x, y axis, clip region, etc.
     */ 
    initChart() {
      let vm = this;
      // console.log("init", vm.plotName)

      let div = $(vm.$el).find("#div_history")[0];
      vm.width = div.clientWidth;
      vm.height = div.clientHeight - vm.uiHeight;
      if (!vm.plotData || Object.keys(vm.plotData).length === 0 
          || vm.width <= 0 || vm.height <= 0) {
        // view is not properly initialized yet, reset width and height back
        vm.width = 0
        vm.height = 0
        return;
      }

      // contentWidth, contentHeight doesn't include the axis
      vm.contentWidth = vm.width - vm.margin.left - vm.margin.right;
      vm.contentHeight = vm.height - vm.margin.top - vm.margin.bottom;

      // clear the svg for preparation (in case there are old elements)
      while (div.firstChild) {
        div.removeChild(div.firstChild);
      }

      vm.svg = d3
        .select(div)
        .append("svg")
        .attr("width", vm.width)
        .attr("height", vm.height);

      // initialize the x axis
      if(gvars.newsTimeScaleUTC) {
        vm.xScale = d3.scaleUtc().range([0, vm.contentWidth]);
        vm.xGScale = d3.scaleUtc().range([0, vm.contentWidth]);
      }
      else {
        vm.xScale = d3.scaleTime().range([0, vm.contentWidth]);
        vm.xGScale = d3.scaleTime().range([0, vm.contentWidth]);
      }
      
      vm.xAxis = d3.axisBottom(vm.xScale).ticks(Math.max(vm.width / 90, 2));
      vm.xAxisGrid = d3.axisBottom(vm.xScale).tickSize(-vm.contentHeight).tickFormat('').ticks(Math.max(vm.width / 90, 2));

      // initialize the left y axis
      vm.yScaleLeft = d3
        .scaleLinear()
        .range([
          vm.contentHeight - gvars.circleMarkerRadius * 2,
          gvars.circleMarkerRadius * 2,
        ]);
      vm.yAxisLeft = d3.axisLeft(vm.yScaleLeft).ticks(Math.max(vm.height / 25, 2));

      // initialize the right y axis, no matter the view will have right axis or not
      vm.yScaleRight = d3
        .scaleLinear()
        .range([
          vm.contentHeight - gvars.circleMarkerRadius * 2,
          gvars.circleMarkerRadius * 2,
        ]);
      vm.yAxisRight = d3.axisRight(vm.yScaleRight).ticks(Math.max(vm.height / 25, 2));

      // prepare a clipping region for zoom and hide out of boundary part
      vm.svg
        .append("defs")
        .append("svg:clipPath")
        .attr("id", vm.plotName.replace(/[^A-Z0-9]+/gi, "_") + "_clip_region")
        .append("svg:rect")
        .attr("x", 0)
        .attr("y", 0)
        .attr("width", vm.contentWidth)
        .attr("height", vm.contentHeight);

      // ------------------------- 1. g_canvas -------------------------
      // the g_canvas = horizontal axis, vertical axis, chart content, rect_zoom, y label, foreignobject
      vm.g_canvas = vm.svg
        .append("g")
        .attr("class", "g_canvas")
        .attr(
          "transform",
          "translate(" + vm.margin.left + "," + vm.margin.top + ")"
        );

      // x axis on the bottom
      vm.g_canvas
        .append("g")
        .attr("class", "axis axis--x  axis-tick")
        .attr("transform", "translate(0," + vm.contentHeight + ")");

      // x axis grid
      vm.g_canvas
        .append("g")
        .attr("class", "axis axis--x--grid axis-grid")
        .attr("transform", "translate(0," + vm.contentHeight + ")");

      // y axis on the left
      vm.g_canvas.append("g").attr("class", "axis axis--y");

      // y axis grid
      vm.g_canvas.append("g").attr("class", "axis axis--y--grid axis-grid");

      // y axis on the right
      vm.g_canvas
        .append("g")
        .attr("class", "axis axis--y-right  axis-tick")
        .attr("transform", "translate(" + vm.contentWidth + ", 0)");

      vm.drawAxisName()

      // the horizontal and vertical cursor lines
      vm.drawCursorLines();

      // ------------------------- 2. g_clip_content -------------------------
      // the g where the clipped zoomable elements will be drawn onto
      // 1. the stock curve
      // 2. matched pattern time step (vertical dashed lines)
      vm.g_clip_content = vm.svg
        .append("g")
        .attr("class", "g_clip_content")
        .attr(
          "transform",
          "translate(" + vm.margin.left + "," + vm.margin.top + ")"
        )
        .attr(
          "clip-path",
          "url(#" + vm.plotName.replace(/[^A-Z0-9]+/gi, "_") + "_clip_region)"
        );

      // projection_line highlighting (vertical dashed lines in red, currend prediction date)
      vm.g_clip_content
        .append("path")
        .attr("id", "path_projection_line")
        .attr("class", "path_projection_line")
        .style("fill", "none")
        .style("stroke", "red")
        .style("stroke-width", "2px")
        .style("stroke-dasharray", "4,3")
        .attr("d", "");

      // ------------------------- 3. g_interact -------------------------
      vm.g_interact = vm.svg
        .append("g")
        .attr("class", "g_interact")
        .attr(
          "transform",
          "translate(" + vm.margin.left + "," + vm.margin.top + ")"
        )
        .attr(
          "clip-path",
          "url(#" + vm.plotName.replace(/[^A-Z0-9]+/gi, "_") + "_clip_region)"
        );

      vm.rect_zoom = vm.g_interact
        .append("rect")
        .attr("class", "zoom")
        .attr("width", vm.contentWidth)
        .attr("height", vm.contentHeight)
        .style("fill", "none")
        .style("cursor", "move")
        .style("pointer-events", "all")
        .on("mousemove", function () {
          // update the highlighted curve line (both horizontal and vertical)
          if (vm.cursorLabel) {
            var mouse = d3.mouse(this);
            vm.updateCursorLines(mouse);
          }
        })
        .on("click", function() {
          var mouse = d3.mouse(this);
          // console.log(mouse)
          var xval = vm.xScale.invert(mouse[0]);
          // let timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
          // var timeStr = xval.toLocaleString("en-US", { timeZone: timezone })
          // console.log(timeStr)
          // console.log(+xval)

          bus.$emit("fetch_one_day_news", {'curAsset': vm.curAsset, 'curDate': (+xval)})
        })

      vm.zoom = d3
        .zoom()
        .scaleExtent([1, 1000])
        .translateExtent([
          [0, 0],
          [vm.contentWidth, vm.contentHeight],
        ])
        .extent([
          [0, 0],
          [vm.contentWidth, vm.contentHeight],
        ])
        .on("zoom", vm.zoomed);

      vm.rect_zoom.call(vm.zoom);

      vm.initialized = true;
    },

    // the name of the y axes (both left and right)
    drawAxisName() {
      let vm = this;
      if(!vm.g_canvas) {
        return;
      }
      
      var axisNameData = []
      if(vm.yLeftField.name.toLowerCase()=='price') {
        axisNameData.push('Price')
      }
      else{
        // no translation, just push the raw text
        axisNameData.push(vm.yLeftField.name)
      }
      if(vm.yRightField && (!vm.shareLeftField)) {
        // yRightField exists and not sharing axis with the left axis
        if(vm.yRightField.name.toLowerCase()=='similarity' 
          || vm.yRightField.name.toLowerCase()=='match') {
            axisNameData.push('Match')
        }
        else {
          // no translation, just push the raw text
          axisNameData.push(vm.yRightField.name)
        }
      } 

      var text_axisName = vm.g_canvas.selectAll(".text_axis_name").data(axisNameData)

      text_axisName
        .enter()
        .append("text")
        .attr("class", "text_axis_name")
        .attr("x", function(d, i) {
          return (i*(vm.contentWidth-10));
        })
        .attr("y", 5)
        .text(function(d) { 
          return d; 
        })
        .attr("text-anchor", "middle")
        .attr("fill", function(d, i) {
          return gvars.curve_clr1[i]
        })
      
      text_axisName
        .text(function(d) { return d; })

      text_axisName.exit().remove()
    },

    // give vm.yRightField, vm.yScaleRight if plotting using the right axis
    linePath(field_name, yScale, curve_type=d3.curveLinear) {
      let vm = this;
      return d3
        .line()
        .x(function (d) {
          return vm.xScale(+d["Date"]);
        })
        .y(function (d) {
          return yScale(+d[field_name]);
        })
        .curve(curve_type);
    },

    updateXAxisScale() {
      let vm = this;
      if (!vm.plotData || Object.keys(vm.plotData).length===0
          || vm.width <= 0 || vm.height <= 0) {
        return;
      }

      vm.xScale.domain([vm.cur_zoom_range_left, vm.cur_zoom_range_right]);
      vm.xAxis = d3.axisBottom(vm.xScale);
      vm.g_canvas.select(".axis--x").call(vm.xAxis);
      vm.g_canvas.select(".axis--x--grid").call(vm.xAxisGrid);
    },

    updateXGAxisScale(updateLocalScale = false) {
      let vm = this;

      if (!vm.plotData || Object.keys(vm.plotData).length===0
          || vm.width <= 0 || vm.height <= 0) {
        return;
      }

      var x_range = [Infinity, -Infinity]

      var allKeys = Object.keys(vm.plotData)
      for(var i=0; i<allKeys.length; i++) {
        var dateAry = d3.extent(vm.plotData[allKeys[i]].map(function(d) {return d['Date']; }))
        if(dateAry[0] < x_range[0]) {
          x_range[0] = dateAry[0]
        }
        if(dateAry[1] > x_range[1]) {
          x_range[1] = dateAry[1]
        }
      }

      // the global scale, that allows us to zoom back
      vm.xGScale.domain([
        x_range[0] - (x_range[1] - x_range[0]) * vm.xMarginRatio,
        x_range[1] + (x_range[1] - x_range[0]) * vm.xMarginRatio,
      ]);

      // if the local xScale also needs to be updated, update it
      if (updateLocalScale) {
        vm.xScale.domain(vm.xGScale.domain());
        vm.xAxis = d3.axisBottom(vm.xScale);
        vm.g_canvas.select(".axis--x").call(vm.xAxis);
        vm.g_canvas.select(".axis--x--grid").call(vm.xAxisGrid);
      }
    },

    updateYAxisScale(yField, yScale, yAxis, axisDomClass, leftOrRight='Left') {
      let vm = this;
      if (!vm.plotData 
          || Object.keys(vm.plotData).length===0
          || (!yField)
          || vm.width <= 0 || vm.height <= 0) {
        return;
      }

      var visibleData = vm.plotData[yField.field].filter(function (d) {
        return (
          +d["Date"] >= +vm.cur_zoom_range_left &&
          +d["Date"] <= +vm.cur_zoom_range_right
        );
      });

      ///---------- 2. compute yScale ----------
      var y_range = [0, 0]
      if(yField.type=="Curve") {
        y_range = d3.extent(
          visibleData.map(function (d) {
            return d[yField.key];
          })
        );
      }
      else if(yField.type=="StackedBar") {
        y_range[1] = d3.max(visibleData, d => {
          // Is there a better way to do this than calling each key?
          var val = 0
          for(var k of yField.key){
            val += d[k]
          }
          return val
        })
      }

      if (y_range[1] == y_range[0]) {
        // avoid corner case where min==max
        y_range[1] = y_range[0] + 1;
      }

      /// ---------- 3. update y_axis ----------
      yScale.domain([
        y_range[0] - (y_range[1] - y_range[0]) * vm.yMarginRatio,
        y_range[1] + (y_range[1] - y_range[0]) * vm.yMarginRatio,
      ]);
      if(leftOrRight=='Left') {
        yAxis = d3.axisLeft(yScale).ticks(Math.max(vm.height / 25, 2));
        vm.yAxisGrid = d3.axisLeft(yScale).tickSize(-vm.contentWidth).tickFormat('').ticks(Math.max(vm.height / 25, 2));
        vm.g_canvas.select(axisDomClass).call(yAxis);
        vm.g_canvas.select(".axis--y--grid").call(vm.yAxisGrid);
      }
      else {
        yAxis = d3.axisRight(yScale).ticks(Math.max(vm.height / 25, 2));
        vm.g_canvas.select(axisDomClass).call(yAxis);
      }
      
    },

    updateYAxisScaleWithBothFieldData(yFieldLeft, yFieldRight, yScale, yAxis, axisDomClass, leftOrRight='Left') {
      let vm = this;
      if (!vm.plotData 
          || Object.keys(vm.plotData).length===0
          || (!yFieldLeft)
          || (!yFieldRight)
          || vm.width <= 0 || vm.height <= 0) {
        return;
      }

      function getRange(yField) {
        if(!vm.plotData.hasOwnProperty(yField.field)) {
          return [0, 1]
        }
        
        var visibleData = vm.plotData[yField.field].filter(function (d) {
          return (
            +d["Date"] >= +vm.cur_zoom_range_left &&
            +d["Date"] <= +vm.cur_zoom_range_right
          );
        });

        ///---------- 2. compute yScale ----------
        var y_range = [0, 0]
        if(yField.type=="Curve") {
          y_range = d3.extent(
            visibleData.map(function (d) {
              return d[yField.key];
            })
          );
        }
        else if(yField.type=="StackedBar") {
          y_range[1] = d3.max(visibleData, d => {
            // Is there a better way to do this than calling each key?
            var val = 0
            for(var k of yField.key){
              val += d[k]
            }
            return val
          })
        }

        if (y_range[1] == y_range[0]) {
          // avoid corner case where min==max
          y_range[1] = y_range[0] + 1;
        }
        return y_range
      }

      var rangeLeft = getRange(yFieldLeft)
      var rangeRight = getRange(yFieldRight)

      var y_range = [0, 0]
      y_range[0] = d3.min([rangeLeft[0], rangeRight[0]])
      y_range[1] = d3.max([rangeLeft[1], rangeRight[1]])

      /// ---------- 3. update y_axis ----------
      yScale.domain([
        y_range[0] - (y_range[1] - y_range[0]) * vm.yMarginRatio,
        y_range[1] + (y_range[1] - y_range[0]) * vm.yMarginRatio,
      ]);
      if(leftOrRight=='Left') {
        yAxis = d3.axisLeft(yScale).ticks(Math.max(vm.height / 25, 2));
        vm.yAxisGrid = d3.axisLeft(yScale).tickSize(-vm.contentWidth).tickFormat('').ticks(Math.max(vm.height / 25, 2));
        vm.g_canvas.select(axisDomClass).call(yAxis);
        vm.g_canvas.select(".axis--y--grid").call(vm.yAxisGrid);
      }
      else {
        yAxis = d3.axisRight(yScale).ticks(Math.max(vm.height / 25, 2));
        vm.g_canvas.select(axisDomClass).call(yAxis);
      }
    },

    getVisibleData(allData) {
      let vm = this;
      var sliceDdata = {}
      var allKeys = Object.keys(allData)

      for(let i=0; i<allKeys.length; i++) {
        let oneKeyData = allData[allKeys[i]].filter(function (d, i) {
          return (
            d["Date"] >= vm.cur_zoom_range_left &&
            d["Date"] <= vm.cur_zoom_range_right
          );
        });
        sliceDdata[allKeys[i]] = oneKeyData
      }

      // // subsampling when data is too large
      // if (slice_data.length > 2 * gvars.maxStockCurvePointForSampling) {
      //   let sample_every = Math.floor(
      //     slice_data.length / gvars.maxStockCurvePointForSampling
      //   );
      //   slice_data = slice_data.filter(function (
      //     value,
      //     index,
      //     Arr
      //   ) {
      //     return index % sample_every == 0;
      //   });
      // }
      return sliceDdata
    }, 

    drawTimeSeries(dom, curveData, cssCurveName, fieldName, yScale, color) {
      let vm = this;

      if(!(curveData && curveData.length>0)) {
        return
      }

      var path_curve_data = [fieldName]
      var path_curve = dom
        .selectAll("."+cssCurveName)
        .data(path_curve_data);

      path_curve
        .enter()
        .append("path")
        .attr("class", cssCurveName)
        .attr("id", (d, i) => {
          return "path_curve_" + d;
        })
        .attr("fill", "none")
        .attr("stroke", color)
        .style("stroke-width", "1.5px")
        .each(function (d, i) {
          if (curveData.length > 0) {
            d3.select(this)
              .datum(curveData)
              .attr("d", vm.linePath(d, yScale))
          }
        });

      path_curve
        .attr("id", (d, i) => {
          return "path_curve_" + d;
        })
        .attr("stroke", color)
        .each(function (d, i) {
          if (curveData.length > 0) {
            d3.select(this)
              .datum(curveData)
              .attr("d", vm.linePath(d, yScale))
          }
        });

      path_curve.exit().remove();
    },

    drawStackedBars(dom, data, keys, cssName) {
      if(!data || data.length==0) {
        return;
      }

      let vm = this;

      var stack = d3.stack().keys(keys)(data)
      stack.map((d,i) => {
        d.map(d => {
          d.key = keys[i]
          return d
        })
        return d
      })

      // Append rectangles
      var g_stacks = dom
        .selectAll("."+cssName)
        .data(stack);

      // the time interval between data[1]['Date'] and data[0]['Date']
      // could be 1 day or 3 days (considering weekend gap)
      var unitLength = d3.min([10, vm.xScale(data[1]['Date'])-vm.xScale(data[0]['Date'])])

      g_stacks.enter()
        .append("g")
        .attr("class", cssName)
        .each(function(d, ii) {
          var rects = d3.select(this).selectAll("rect").data(d)

          rects.enter()
            .append("rect")
            .attr('x', (d, i) => vm.xScale(data[i]['Date'])-unitLength*0.45)
            .attr('width', unitLength*0.9)
            .attr('height', d => {
              return vm.yScaleLeft(d[0])-vm.yScaleLeft(d[1])
            })
            .attr('y', d => vm.yScaleLeft(d[1]))
            .style("fill", gvars.area_clr[ii % gvars.area_clr.length])
            .style("fill-opacity", 0.5)
          
          rects.attr('x', (d, i) => vm.xScale(data[i]['Date'])-unitLength*0.45)
            .attr('width', unitLength*0.9)
            .attr('height', d => {
              return vm.yScaleLeft(d[0])-vm.yScaleLeft(d[1])
            })
            .attr('y', d => vm.yScaleLeft(d[1]))
            .style("fill", gvars.area_clr[ii % gvars.area_clr.length])
            .style("fill-opacity", 0.5)
          
          rects.exit().remove()
        })

      g_stacks.each(function(d, ii) {
        var rects = d3.select(this).selectAll("rect").data(d => d)
          
        rects.enter()
          .append("rect")
          .attr('x', (d, i) => vm.xScale(data[i]['Date'])-unitLength*0.45)
          .attr('width', unitLength*0.9)
          .attr('height', d => {
            return vm.yScaleLeft(d[0])-vm.yScaleLeft(d[1])
          })
          .attr('y', d => vm.yScaleLeft(d[1]))
          .style("fill", gvars.area_clr[ii % gvars.area_clr.length])
          .style("fill-opacity", 0.5)
        
        rects.attr('x', (d, i) => vm.xScale(data[i]['Date'])-unitLength*0.45)
          .attr('width', unitLength*0.9)
          .attr('height', d => {
            return vm.yScaleLeft(d[0])-vm.yScaleLeft(d[1])
          })
          .attr('y', d => vm.yScaleLeft(d[1]))
          .style("fill", gvars.area_clr[ii % gvars.area_clr.length])
          .style("fill-opacity", 0.5)
        
        rects.exit().remove()
      })

      g_stacks.exit().remove()
    },

    drawLegend(fieldlist) {
        let vm = this;
        if (!vm.plotData 
          || Object.keys(vm.plotData).length===0
          || vm.width <= 0 || vm.height <= 0) {
            return;
        }

        var legend_offset_x = 20
        var legend_offset_y = 20
        var gap_rect_text = 3
        var ea_legend_h = 15
        var ea_legend_w = 150
        var ea_legend_rect_h = 10
        var ea_legend_rect_w = 10
        var legend_per_col = 4

        var g_legend = vm.g_clip_content.selectAll(".g_legend").data(fieldlist)

        g_legend.enter()
            .append("g")
            .attr("class", "g_legend")
            .attr("transform", function(d, i) {
                return "translate(" +
                    (legend_offset_x + ea_legend_w*Math.floor(i/legend_per_col)) +
                    "," +
                    (legend_offset_y + ea_legend_h*(i%legend_per_col)) +
                    ")"
            })
            .each(function(d, i) {
                d3.select(this)
                    .append("rect")
                    .attr("x", 0)
                    .attr("y", 0)
                    .attr("width", ea_legend_rect_w)
                    .attr("height", ea_legend_rect_h)
                    .style("fill", gvars.area_clr[i % gvars.area_clr.length])
                    .style("fill-opacity", 0.5)
                
                d3.select(this)
                    .append("text")
                    .attr("dx", gap_rect_text+ea_legend_rect_w)
                    .attr("dy", ea_legend_rect_h)
                    .attr("font-size", "12px")
                    .attr("fill", "gray")
                    .text(d)
            })

        g_legend
            .each(function(d, i) {
                d3.select(this)
                    .select("rect")
                    .attr("fill", gvars.area_clr[i % gvars.area_clr.length])
                
                d3.select(this)
                    .select("text")
                    .text(d)
            })

        g_legend.exit().remove()
    },

    // the stock closing price curve
    drawStockCurve() {
      let vm = this;

      if (!vm.plotData || Object.keys(vm.plotData).length===0
         || vm.width <= 0 || vm.height <= 0) {
        return;
      }

      //! Step 1 slice data to the current zoomed range
      vm.visPartData = vm.getVisibleData(vm.plotData)

      //! Step 2 update x scale
      vm.updateXAxisScale();
      
      //! Step 3 draw curve data using the left and right axes
      if(vm.yLeftField){
        if(vm.shareLeftField && vm.yRightField) {
          // update the left axis with date from both left and rigth field
          vm.updateYAxisScaleWithBothFieldData(vm.yLeftField, vm.yRightField, vm.yScaleLeft, vm.yAxisLeft, ".axis--y", 'Left')
        }
        else {
          // update left axis with only the left field data
          vm.updateYAxisScale(vm.yLeftField, vm.yScaleLeft, vm.yAxisLeft, ".axis--y", 'Left')
        }

        if(vm.yLeftField.type=="Curve") {
          vm.drawTimeSeries(vm.g_clip_content, 
                      vm.visPartData[vm.yLeftField.field], "path_curve", 
                      vm.yLeftField.key, vm.yScaleLeft, gvars.curve_clr1[0])
        }
        else if(vm.yLeftField.type=="StackedBar") {
          vm.drawStackedBars(vm.g_clip_content, 
                      vm.visPartData[vm.yLeftField.field], 
                      vm.yLeftField.key, "g_stacked_bar")
          vm.drawLegend(vm.yLeftField.key)
        }
        
      }

      //! Step 4. draw the markers if needed 
      if(vm.zoomRedDot) {
        vm.drawStepMarkers();
      }

      //! Step 5. draw the second curve using the right axis (only if the plot is for curve)
      if(vm.yRightField){
        if(vm.shareLeftField) {
          if(vm.yLeftField.type=="Curve") {
            // draw the right curve using the left axis and scale
            vm.drawTimeSeries(vm.g_clip_content, 
                          vm.visPartData[vm.yRightField.field], "path_curve_right", 
                          vm.yRightField.key, vm.yScaleLeft, gvars.curve_clr1[1])
          }
        }
        else {
          // update the right axis scale, and use it for drawing
          vm.updateYAxisScale(vm.yRightField, vm.yScaleRight, vm.yAxisRight, ".axis--y-right", 'Right')
          if(vm.yLeftField.type=="Curve") {
            vm.drawTimeSeries(vm.g_clip_content, 
                          vm.visPartData[vm.yRightField.field], "path_curve_right", 
                          vm.yRightField.key, vm.yScaleRight, gvars.curve_clr1[1])
          }
        }
        
      }
    },

    // red point markers when zooming into the stock curve
    drawStepMarkers() {
      let vm = this;
      if (!vm.plotData || Object.keys(vm.plotData).length===0
          || vm.width <= 0 || vm.height <= 0 || (!vm.zoomRedDot)) {
        return;
      }

      var yPrimary = vm.yLeftField
      var yScale = vm.yScaleLeft
      if(vm.primaryAxis=='Left') {
        yPrimary = vm.yLeftField
        yScale = vm.yScaleLeft
      }
      else {
        yPrimary = vm.yRightField
        yScale = vm.yScaleRight
      }

      function getMarkerData() {
        if(!(vm.plotData && vm.plotData.hasOwnProperty(yPrimary.field))) {
          return []
        }
        var start_idx = 0;
        var end_idx = vm.plotData[yPrimary.field].length - 1;
        if (
          d3.timeDay.count(vm.cur_zoom_range_left, vm.cur_zoom_range_right) <
          gvars.show_node_when_lessthan
        ) {
          // zoom into threshold, slice data
          // find largest existing date in earlier than date[0]
          var index = vm.plotData[yPrimary.field].findIndex((o) => {
            // findIndex return THE FIRST index satisfying the querry
            // the array g_date is traversed from left
            return d3.timeDay.count(o["Date"], vm.cur_zoom_range_left) < 7; // use a week as buffer
          });

          for (var i = index; i < vm.plotData[yPrimary.field].length - 1; i++) {
            if (
              vm.plotData[yPrimary.field][i]["Date"] < vm.cur_zoom_range_left &&
              vm.plotData[yPrimary.field][i + 1]["Date"] >= vm.cur_zoom_range_left
            ) {
              start_idx = i;
              break;
            }
          }

          //find smallest existing date that is larter than date[1]
          var index = vm.plotData[yPrimary.field].findIndex((o) => {
            return d3.timeDay.count(vm.cur_zoom_range_right, o["Date"]) >= 1;
          });
          for (var i = index; i >= 1; i--) {
            if (
              vm.plotData[yPrimary.field][i]["Date"] > vm.cur_zoom_range_right &&
              vm.plotData[yPrimary.field][i - 1]["Date"] < vm.cur_zoom_range_right
            ) {
              end_idx = i;
              break;
            }
          }

          // if the current model is hourly, then need the following code to keep skip data slicing
          if (end_idx - start_idx + 1 > gvars.show_node_when_lessthan) {
            return [];
          } else {
            return vm.plotData[yPrimary.field].slice(start_idx, end_idx + 1); // include the last element when slicing
          }
        } else {
          // the zoom is not detailed enough, do not show the circles
          return [];
        }
      }

      vm.markerData = getMarkerData();

      var circle_markers = vm.g_interact
        .selectAll(".circle_marker")
        .data(vm.markerData);

      // enter
      circle_markers
        .enter()
        .append("circle")
        .attr("class", "circle_marker")
        .on("click", function (d, i) {
          d3.selectAll(".circle_marker").style("fill-opacity", 0.4);
          // d3.select(this).style("fill-opacity", 1)
          vm.cur_proj_time_date = d["Date"]; 
          for (var j = vm.plotData[yPrimary.field].length - 1; j >= 0; j--) {
            if (
              // vm.plotData[j]["Date"].getTime() == d["Date"].getTime()
              vm.plotData[yPrimary.field][j]["Date"] == d["Date"]
            ) {
              vm.cur_proj_time_idx = j;
              break;
            }
          }
          
          // console.log(vm.cur_proj_time_idx, vm.cur_proj_time_date)
          bus.$emit("fetch_one_day_news", {'curAsset': vm.curAsset, 'curDate':vm.cur_proj_time_date})
        })
        .attr("cx", function (d, i) {
          return vm.xScale(+d["Date"]);
        })
        .attr("cy", function (d, i) {
          return yScale(+d[yPrimary.key]);
        })
        .attr("r", gvars.circleMarkerRadius)
        .style("fill", function (d, i) {
          return "red";
        })
        .style("fill-opacity", 0.4)
        .style("stroke", "none");

      // update
      circle_markers
        // .attr("id", function (d) {
        //   return "circle_marker_" + d.step;
        // })
        .attr("cx", function (d, i) {
          return vm.xScale(+d["Date"]);
        })
        .attr("cy", function (d, i) {
          return yScale(+d[yPrimary.key]);
        })
        .style("fill-opacity", 0.4);

      // exit
      circle_markers.exit().remove();
    },

    zoomed() {
      let vm = this;
      if (d3.event.sourceEvent && d3.event.sourceEvent.type === "brush") return; // ignore zoom-by-brush
      var t = d3.event.transform;

      gvars.trans = t;

      vm.cur_zoom_range_left = t.rescaleX(vm.xGScale).domain()[0];
      vm.cur_zoom_range_right = t.rescaleX(vm.xGScale).domain()[1];

      if (!vm.disableEventDispatch) {
        bus.$emit("linePlot_sync_zoom");
      }

      // update the cursor label lines
      if (vm.cursorLabel) {
        var mouse = d3.mouse(vm.rect_zoom.node());
        vm.updateCursorLines(mouse);
      }
    },

    // the mouse cursor, the horizontal line, the vertical line, and the square on current value
    drawCursorLines() {
      let vm = this;

      if (!vm.plotData || Object.keys(vm.plotData)===0 
          || vm.width <= 0 || vm.height <= 0) {
        return;
      }

      vm.g_canvas.select("#g_x_cursor_label").remove();
      vm.g_canvas.select("#g_y_cursor_label").remove();
      vm.g_canvas.select("#g_cursor_point").remove();
      if (!vm.cursorLabel) {
        return;
      }
      
      // vertical line and x label
      vm.g_canvas
        .append("g")
        .attr(
          "transform",
          "translate(" +
            0 +
            "," +
            (vm.margin.top + vm.contentHeight - vm.xCursorLabelHeight / 2) +
            ")"
        )
        .attr("id", "g_x_cursor_label")
        .style("fill-opacity", 0)
        .style("stroke-opacity", 0)
        .each(function () {
          // the vertical line
          d3.select(this)
            .append("path")
            .attr(
              "d",
              "M 0 0 L 0 " +
                (-vm.margin.top -
                  vm.contentHeight -
                  vm.xCursorLabelHeight / 2)
            )
            .style("stroke", "gray")
            .style("stroke-dasharray", "5,2");

          // the text on x
          d3.select(this)
            .append("rect")
            .attr("x", 0)
            .attr("y", 0)
            .attr("rx", 1)
            .attr("ry", 1)
            .attr("width", vm.xCursorLabelWidth)
            .attr("height", vm.xCursorLabelHeight)
            .style("stroke", "black")
            .style("fill", "gray");

          d3.select(this)
            .append("text")
            .attr("x", 6)
            .attr("y", vm.xCursorLabelHeight - 6)
            .attr("font-size", 11)
            .style("fill", "white");
        });

      // horizontal line and y label
      vm.g_canvas
        .append("g")
        .attr("transform", "translate(" + 0 + "," + -100 + ")")
        .attr("id", "g_y_cursor_label")
        .style("fill-opacity", 0)
        .style("stroke-opacity", 0)
        .each(function () {
          d3.select(this)
            .append("path")
            .attr("d", "M 0 0 L " + vm.contentWidth + " 0")
            .style("stroke", "gray")
            .style("stroke-dasharray", "5,2");

          d3.select(this)
            .append("rect")
            .attr("x", 0)
            .attr("y", -25)
            .attr("rx", 1)
            .attr("ry", 1)
            .attr("width", vm.yCursorLabelWidth)
            .attr("height", vm.yCursorLabelHeight)
            .style("stroke", "black")
            .style("fill", "gray");

          d3.select(this)
            .append("text")
            .attr("x", 10)
            .attr("y", -12)
            .attr("font-size", 11)
            .style("fill", "white");
        });

      // the current data point
      vm.g_canvas
        .append("g")
        .attr("id", "g_cursor_point")
        .attr("transform", "translate(" + -200 + "," + 0 + ")") // -200 is to hide it initially
        .append("rect")
        .attr("x", -5)
        .attr("y", -5)
        .attr("width", 10)
        .attr("height", 10)
        .attr("stroke", "black")
        .attr("fill", "none");
    },

    updateCursorLines(mouse) {
      bus.$emit('update_cursor_line', mouse)
    },

    _updateCursorLines(mouse) {
      let vm = this;

      if (
        !vm.cursorLabel ||
        !vm.plotData ||
        Object.keys(vm.plotData).length===0 ||
        vm.width <= 0 ||
        vm.height <= 0
      ) {
        return;
      }

      //! 1. compute x and move cursor label to cursor_x position
      if (!mouse[0]) return;

      var yPrimary = vm.yLeftField
      var yScale = vm.yScaleLeft
      if(vm.primaryAxis=='Left') {
        yPrimary = vm.yLeftField
        yScale = vm.yScaleLeft
      }
      else {
        yPrimary = vm.yRightField
        yScale = vm.yScaleRight
      }

      if(!(vm.visPartData && vm.visPartData.hasOwnProperty(yPrimary.field))) {
        return
      }
      var xval = vm.xScale.invert(mouse[0]);

      vm.g_canvas
        .select("#g_x_cursor_label")
        .style("fill-opacity", 1)
        .style("stroke-opacity", 1)
        .attr(
          "transform",
          "translate(" +
            vm.xScale(xval) +
            "," +
            (vm.margin.top + vm.contentHeight - vm.xCursorLabelHeight / 2) +
            ")"
        )
        .each(function () {
          let timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
          if (vm.xScale(xval) + vm.xCursorLabelWidth > vm.contentWidth) {
            // reposition the label if it is out of the horizontal boundary
            d3.select(this)
              .select("rect")
              .attr(
                "x",
                vm.contentWidth - (vm.xScale(xval) + vm.xCursorLabelWidth)
              );
            d3.select(this)
              .select("text")
              .attr(
                "x",
                vm.contentWidth -
                  (vm.xScale(xval) + vm.xCursorLabelWidth) +
                  5
              )
              .text(function() {
                if(gvars.newsTimeScaleUTC) {
                  return new Date(+xval).toUTCString()
                }
                else {// local time
                  return xval.toLocaleString("en-US", { timeZone: timezone })
                }
              })   
          } else {
            d3.select(this).select("rect").attr("x", 0);
            d3.select(this)
              .select("text")
              .attr("x", 5)
              .text(function() {
                if(gvars.newsTimeScaleUTC) {
                  return new Date(+xval).toUTCString()
                }
                else {// local time
                  return xval.toLocaleString("en-US", { timeZone: timezone })
                }
              });
          }
        });

      // draw the y line (step 2) and cur value (step 3), only available if this is a line chart
      if(vm.yLeftField.type=='Curve') {
        //! 2. compute y and move cursor label to cursor_y position
        var index = vm.visPartData[yPrimary.field].findIndex((o) => {
          // findIndex return THE FIRST index satisfying the querry
          // the array vm.plotData is traversed from left
          return d3.timeDay.count(o["Date"], xval) < 7; // use a week as buffer
        });
        if (index < 0) return;
        var start_idx = 0;
        for (var i = index; i < vm.visPartData[yPrimary.field].length - 1; i++) {
          if (
            vm.visPartData[yPrimary.field][i]["Date"] < xval &&
            vm.visPartData[yPrimary.field][i + 1]["Date"] >= xval
          ) {
            start_idx = i;
            break;
          }
        }

        // compute the ration between two neighboring y values using the x ratio
        var ratio =
          (xval - vm.visPartData[yPrimary.field][start_idx]["Date"]) /
          (vm.visPartData[yPrimary.field][start_idx + 1]["Date"] -
            vm.visPartData[yPrimary.field][start_idx]["Date"]);
        var yval =
          vm.visPartData[yPrimary.field][start_idx][yPrimary.key] +
          ratio *
            (vm.visPartData[yPrimary.field][start_idx + 1][yPrimary.key] -
              vm.visPartData[yPrimary.field][start_idx][yPrimary.key]);

        vm.g_canvas
          .select("#g_y_cursor_label")
          .style("fill-opacity", 1)
          .style("stroke-opacity", 1)
          .attr("transform", "translate(" + 5 + "," + yScale(yval) + ")")
          .each(function () {
            if (yScale(yval) < vm.yCursorLabelWidth) {
              d3.select(this)
                .select("rect")
                .attr("x", yScale(yval) - vm.yCursorLabelWidth)
                .attr("transform", "rotate(-90)");
              d3.select(this)
                .select("text")
                .attr("x", yScale(yval) - vm.yCursorLabelWidth + 10)
                .attr("transform", "rotate(-90)")
                .text(yval.toFixed(2));
            } else {
              d3.select(this)
                .select("rect")
                .attr("x", 0)
                .attr("transform", "rotate(-90)");
              d3.select(this)
                .select("text")
                .attr("x", 10)
                .attr("transform", "rotate(-90)")
                .text(yval.toFixed(2));
            }
          });

        //! 3. move the current point
        vm.g_canvas
          .select("#g_cursor_point")
          .attr(
            "transform",
            "translate(" + vm.xScale(xval) + "," + yScale(yval) + ")"
          );
      }
    },

    /**
     * draw everything
     */
    drawChart() {
      let vm = this;

      if (!vm.plotData || Object.keys(vm.plotData).length===0
          || vm.width <= 0 || vm.height <= 0) {
        return;
      }

      // ! Step 1. update stock curve
      vm.drawStockCurve();

      // // ! Step 2. this is the vertical starting line for the projection
      // vm.drawPrejectionStartingLine();

      // // ! Step 3. this is the aggregated projection std and mean curve
      // vm.drawProjections();

      // // ! Step 4. update the historical matched lines (vertical lines)
      // vm.drawMatchedLines();

      // // ! Step 5. update the trading decisions, this is the triangle for buy/sell
      // vm.drawTradingDecisions();
    },

    /**
     * callback for the zoom button
     * when global==1, reset the zoom
     * when global==0, zoom into the last n points
     */
    onClickBtnZoomSet(global) {
      let vm = this;

      if (!vm.plotData || Object.keys(vm.plotData).length===0) {
        return;
      }

      /**
       * set the zoom range for the new data
       * set gloal trans to empty means using 
       * the cur_zoom_range to compute the global trans
       */
      gvars.trans = {};

      // set to the latest zoom scale
      var zoom_step = 0
      if (global) {
        /**
         * should set to the default zoom scale
         * num_default_steps_to_show is a number larger than plotData.length
         */
        zoom_step = gvars.num_default_steps_to_show;
        vm.asset_curve_zoom_recent = false;
      } else {
        // num_latest_steps_to_show is like 150
        zoom_step = gvars.num_latest_steps_to_show;
        vm.asset_curve_zoom_recent = true;
      }

      var yPrimary = vm.yLeftField
      if(vm.primaryAxis=='Left') {
        yPrimary = vm.yLeftField
      }
      else {
        yPrimary = vm.yRightField
      }
      if(vm.plotData && vm.plotData.hasOwnProperty(yPrimary.field)) {
        if (vm.plotData[yPrimary.field].length < zoom_step) {
          vm.cur_zoom_range_left = vm.plotData[yPrimary.field][0]["Date"];
        } else {
          vm.cur_zoom_range_left =
            vm.plotData[yPrimary.field][vm.plotData[yPrimary.field].length - zoom_step]["Date"];
        }
        vm.cur_zoom_range_right = vm.plotData[yPrimary.field][vm.plotData[yPrimary.field].length - 1]["Date"];
        bus.$emit("linePlot_sync_zoom");
      }
    },

    syncZoom() {
      let vm = this;

      // stop zoom, if there is no data
      if (Object.keys(vm.plotData).length===0 || !vm.xGScale || !vm.rect_zoom) {
        return;
      }

      // stop zoom if the current zoom range contains less than 10 points/days
      if (
        vm.cur_time_scale == "1d" &&
        d3.timeDay.count(vm.cur_zoom_range_left, vm.cur_zoom_range_right) < 10
      ) {
        return;
      }

      // stop zoom if the current zoom range contains less than 10 points/hours
      if (
        vm.cur_time_scale == "1h" &&
        d3.timeHour.count(vm.cur_zoom_range_left, vm.cur_zoom_range_right) < 10
      ) {
        return;
      }

      /**
       * stop sending the syncZoom event, while we are zooming
       * i.e., while we calling the vm.rect_zoom.call()
       */
      vm.disableEventDispatch = 1;

      if (Object.keys(gvars.trans).length === 0) {
        // if the global transformation matrix has not been set up yet
        // zoom from the rightmost point
        var kval =
          (vm.xGScale.range()[1] - vm.xGScale.range()[0]) /
          (vm.xGScale(vm.cur_zoom_range_right) -
            vm.xGScale(vm.cur_zoom_range_left));
        var xval = vm.xGScale.range()[1] - vm.xGScale.range()[1] * kval;

        /**
         * this function will call the zoomed(),
         * make sure disableEventDispatch==1
         * to prevent endless recursive call
         */
        vm.rect_zoom.call(
          vm.zoom.transform,
          d3.zoomIdentity.translate(xval, 0).scale(kval)
        );
      } else {
        /**
         * if the gloabl transformation matrix has been set
         * just zoom into that matrix specified range
         */
        vm.rect_zoom.call(vm.zoom.transform, gvars.trans);
      }

      vm.drawChart();

      // enable the zoom event dispatch after the current zooming
      vm.disableEventDispatch = 0;
    },

    divResize() {
      let vm = this;
      let div = $(vm.$el).find("#div_history")[0];

      /**
       * when leaving a tab, the width and heigh to the div will become 0
       * but we don't need to initialize and redraw the view, so skip
       */
      if(div.clientWidth<=0 || div.clientHeight<=0) {
        return;
      }

      /**
       * if the width is the same with the early initialized width
       * no need to initialize and redraw the view
       * For example, if switch from tab 1 to tab 2, tab 1's 
       * clientWidth becomes 0, the above if-statement skips this function
       * So, tab 1's vm.width is not changed (though its clientWidth become 0)
       * then swtich from tab 2 back to tab 1 (tab 1's clientWidth 
       * is now the same with its vm.width), in this process, tab 1 should not
       * be recreated to maintatin its transformation matrix
       */
      if(div.clientWidth==vm.width && (div.clientHeight-vm.uiHeight)==vm.height) {
        return;
      }

      vm.width = div.clientWidth;
      vm.height = div.clientHeight - vm.uiHeight;
      if (vm.width <= 0 || vm.height <= 0) {
        return;
      } else {
        vm.initChart();

        vm.updateXGAxisScale();

        // if (
        //   (vm.projectionCurves && vm.matchedLines.length == 0) ||
        //   (vm.projectionCurves && vm.coneData.length == 0)
        // ) {
        //   // need to recomputed the matched lines based on the projectionCurves
        //   // there are possible cases that the watcher of projectionCuves is not catched
        //   // so we do this if branch to guarantee the matched lines are computed
        //   vm.updateProjectionCurve();
        // }

        vm.drawChart();
      }
    }
  },

  // created() {
  //   window.addEventListener("resize", this.windowResizeEventHandler);
  // },
  // destroyed() {
  //   window.removeEventListener("resize", this.windowResizeEventHandler);
  // },
  mounted() {
    let vm = this;

    /**
     * this detect when the div is resized
     * this function will also be triggered if you swtich between tabs
     * when you switch away from a tab, the div.clientWidth becomes 0
     * 
     * window resize will trigger div resize, so window resize is also observed
     * in contrast, windowResizeEventHandler only detect window resize
     */
    new ResizeObserver(vm.divResize).observe(vm.$el);

    bus.$on("linePlot_sync_zoom", function () {
      /**
       * if the current tab is not in selection, no need to zoom, this
       * will increase the preformance. However, make sure this event
       * is emitted when switching between tabs, to sync the transformation
       * when switching tab
       */
      // if(vm.curTabName!=vm.parentTabName) {
      //   return
      // }
      if (!vm.initialized) {
        vm.initChart();
      }
      vm.syncZoom();
    });

    bus.$on('update_cursor_line', function(mouse) {
      vm._updateCursorLines(mouse)
    })

    bus.$on('update_plot_data_partially', function() {
      vm.onClickBtnZoomSet(0);
    })

    // // the dispatch event are only for external vue to call
    // bus.$on("linePlot_update_xaxis_scale", function () {
    //   if (!vm.initialized) {
    //     vm.initChart();
    //   }
    //   vm.updateXAxisScale();
    // });

    // bus.$on("linePlot_update_yaxis_scale", function () {
    //   vm.updateYAxisScale();
    // });

    // // if updateLocalScale is true, the local xScale will also be updated
    // bus.$on("linePlot_update_xgaxis_scale", function (updateLocalScale) {
    //   if (!vm.initialized) {
    //     vm.initChart();
    //   }
    //   vm.updateXGAxisScale(updateLocalScale);
    // });

    // bus.$on("projectionCard_click_one_match", function (d) {
    //   if (!vm.initialized) {
    //     vm.initChart();
    //   }
    //   vm.highlightMatchedCurveMame = d;
    //   vm.drawMatchedLines();
    // });

    // bus.$on("event_change_language", function() {
    //   vm.drawAxisName()
    // })
  },
};
</script>

<style scoped>
@keyframes draw_dash {
  from {
    stroke-dashoffset: 0;
    stroke-width: 5;
  }
  to {
    stroke-dashoffset: 30000;
    stroke-width: 5;
  }
}

.widget-button {
  background-color: rgba(0, 0, 0, 0);
  border-style: none;
  font-size: 12px;
  padding: 0px 30px;
}

/* .path_yello {
  stroke: rgb(236,191,110);
  stroke-width: 1.2pt;
}

.path_purple {
  stroke: rgb(88,57,217); 
  stroke-width: 1.2pt;
}

.rect_yello {
  fill: rgb(236,191,110);
}

.rect_purple {
  fill: rgb(88,57,217); 
} */


</style>
