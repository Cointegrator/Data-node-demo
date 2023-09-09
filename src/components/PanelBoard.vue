<template>
  <b-container class="bv-example-row" fluid>
  <b-row>
    <!-- the left panel -->
    <b-col class="col-6">
      <b-card no-body>
        <template #header>
          <div class="div-header">
            <h6>My Market AI Agent (demand monitor)</h6>
          </div>
        </template>
        <b-row>
          <div class="div-content">
            
            <el-table stripe style="width: 100%" :data="visibleData" border>
              <el-table-column
                sortable
                v-for="column in tableColumns"
                :key="column.label"
                :min-width="column.minWidth"
                :prop="column.prop"
                :label="column.label"
              >
              </el-table-column>
            </el-table>
          </div>
        </b-row>
      </b-card>
    </b-col>

    <!-- the right panel -->
    <b-col class="col-6">
      <b-card no-body>
        <template #header>
          <div class="div-header">
            <h6>My Uploading Agent (supply monitor)</h6>
          </div>
        </template>
        <b-row>
          <div class="div-content">
            <history-plot
              plot-name="semantic_curve"
              :plot-data="plotData"
              :zoom-red-dot='false'
              :y-left-field="{
                type: 'Curve',
                name: 'Price',  // show this as the axis name
                field: 'price', // this is the ts field of plotData
                key: 'Close',   // this is the yaxis key (x-axis is Date)
              }"
              :y-right-field="{ 
                type: 'Curve', 
                name: 'Sentiment', 
                field: 'sentiment',
                key: 'Sentiment',
              }"
              :div-height="26"
              style="width:100%"
            >
            </history-plot>
          </div>
        </b-row>
      </b-card>
    </b-col>
  </b-row>
</b-container>
</template>

<script>
import axios from "axios";
import HistoryPlot from './HistoryPlot.vue';
export default {
  name: 'PanelBoard',
  props: {
    msg: String
  },
  components: {
    HistoryPlot
  },
  data() {
    return {
      visibleData: [],
      tableColumns: [
        {
          prop: "asset_name",
          label: "Name",
          minWidth: 100,
        },
        {
          prop: "feature_0",
          label: "feature_0",
          minWidth: 150,
        },
        {
          prop: "feature_1",
          label: "feature_1",
          minWidth: 130,
        },
        {
          prop: "feature_2",
          label: "feature_2",
          minWidth: 160,
        },
      ],
      
    }
  },
  methods: {
    async loadData() {
      let vm = this;
      // for(var i=0; i<10; i++) {
      //   var obj = {}
      //   obj['asset_name'] = "name_"+i
      //   obj['feature_0'] = "feature_0_"+i
      //   obj['feature_1'] = "feature_1_"+i
      //   obj['feature_2'] = "feature_2_"+i
      //   vm.visibleData.push(obj);
      // }
      
      let path = "http://localhost:5000/getAssetData";
      try {
        const response = await axios.post(path, {
          params: {
            asset_name: 'AAPL'
          },
        });

        vm.visibleData = response.data

      } catch (error) {
        // pop up the error message
        console.log(error.message)
      }
    },

    loadPlotData() {
      let vm = this;
      vm.plotData = {
          'price':[
              {'Date': 1662681600000, 'Close':21364.3},
              {'Date': 1662768000000, 'Close':21652.5},
              {'Date': 1662854400000, 'Close':20652.5},
              {'Date': 1662940800000, 'Close':20252.5},
            ],
          'sentiment': [
              {'Date': 1662681600000, 'Sentiment':0.3},
              {'Date': 1662768000000, 'Sentiment':0.7},
              {'Date': 1662854400000, 'Sentiment':0.5},
              {'Date': 1662940800000, 'Sentiment':0.1},
          ]
        }
    }
  },
  async beforeMount() {
    let vm = this;

    vm.loadPlotData()
    await vm.loadData()    
  },
  mounted() {},
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.div-header {
  /* float: left; */
  font-size: 20pt;
  /* font-style: italic; */
}

.div-content {
  height: 800px;
}
</style>

<style>
 /* 2023-02-11 have to disabble the scoped styles, otherwise d3.classed doesn't work */
.path_baseline {
  stroke: rgb(236,191,110);
  stroke-width: 1.2pt;
}

.path_return {
  stroke: rgb(88,57,217); 
  stroke-width: 1.2pt;
}

.rect_baseline {
  fill: rgb(236,191,110);
}

.rect_return {
  fill: rgb(88,57,217); 
}

/* the style of the grid for time series plot */
.axis-tick .domain{
  stroke: rgb(235,235,235);
}

.axis-tick line{
  stroke: rgb(235,235,235);
}

.axis-tick text{
  fill: gray;
}

.axis-grid line {
  stroke: rgb(235,235,235);
}

.axis-grid .domain {
  stroke: rgb(235,235,235);
}

</style>