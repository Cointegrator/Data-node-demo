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
        <b-row class="div-content">
          <b-col class="col-6">
            <span class="span-table-title">Asset</span>
            <table-plot :table-data="assetData" :table-columns="assetColumns" table-name="assetTable"></table-plot>
          </b-col>
          <b-col class="col-6">
            <span class="span-table-title">System Indicators</span>
            <table-bar-plot 
              :table-data="indicatorData" 
              :table-columns="indicatorColumns"
              bar-col-ref="total"
              bar-col-name="Percentage"
              table-name="indicatorTable"
            >
            </table-bar-plot>
          </b-col>
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
        <b-row class="div-content">
          <b-col>
            <b-row>
              <b-col class="col-12">
                <span class="span-table-title">My Monitor</span>
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
                  :div-height="30"
                  style="width:100%"
                >
                </history-plot>
              </b-col>
            </b-row>
            <b-row>
              <b-col class="col-6">
                <span class="span-table-title">My Indicators</span>
                <table-plot :table-data="tableData" :table-columns="tableColumns"></table-plot>
              </b-col>
              <b-col class="col-6">
                  <span class="span-table-title">Parameters</span>
                  <card-plot :list-data="parameterData"></card-plot>
              </b-col>
            </b-row>
          </b-col>
        </b-row>
        
      </b-card>
    </b-col>
  </b-row>
</b-container>
</template>

<script>
import axios from "axios";
import HistoryPlot from './HistoryPlot.vue';
import TablePlot from './TablePlot.vue';
import TableBarPlot from './TableBarPlot.vue';
import CardPlot from './CardPlot.vue';
export default {
  name: 'PanelBoard',
  props: {
    msg: String
  },
  components: {
    HistoryPlot,
    TablePlot,
    CardPlot,
    TableBarPlot
  },
  data() {
    return {
      tableData: [],
      tableColumns: [
        {
          prop: "asset_name",
          label: "Name",
          minWidth: 50,
        },
        {
          prop: "feature_0",
          label: "feature_0",
          minWidth: 50,
        },
        {
          prop: "feature_1",
          label: "feature_1",
          minWidth: 50,
        },
      ],

      userData: [],
      userColumns: [
        {
          prop: "user_name",
          label: "User Name",
          minWidth: 50,
        },
        {
          prop: "name",
          label: "Name",
          minWidth: 50,
        },
        {
          prop: "email",
          label: "Email",
          minWidth: 50,
        },
      ],
      
      parameterData: [],
      plotData: {
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
        },
      
      
      assetData: [],
      assetColumns: [
        {
          prop: "rank",
          label: "Rank",
          minWidth: 32,
        },
        {
          prop: "name",
          label: "Name",
          minWidth: 50,
        },
        {
          prop: "total",
          label: "Trendy",
          minWidth: 38,
        },
      ],

      indicatorData: [],
      indicatorColumns: [
        {
          prop: "rank",
          label: "Rank",
          minWidth: 32,
        },
        {
          prop: "name",
          label: "Name",
          minWidth: 50,
        },
        // {
        //   prop: "total",
        //   label: "Trendy",
        //   minWidth: 38,
        // },
      ],

    }
  },
  methods: {
    async loadData() {
      let vm = this;      
      let path = "http://localhost:5000/getAssetData";
      try {
        const response = await axios.post(path, {
          params: {
            asset_name: 'AAPL'
          },
        });

        vm.tableData = response.data

      } catch (error) {
        // pop up the error message
        console.log(error.message)
      }
    },

    async loadUserData() {
      let vm = this;      
      let path = "http://localhost:5000/getUsers";
      try {
        const response = await axios.post(path, {
          params: {
            asset_name: 'AAPL'
          },
        });

        vm.userData = response.data

      } catch (error) {
        // pop up the error message
        console.log(error.message)
      }
    },

    async loadPlotData() {
      let vm = this;
      // vm.plotData = {
      //     'price':[
      //         {'Date': 1662681600000, 'Close':21364.3},
      //         {'Date': 1662768000000, 'Close':21652.5},
      //         {'Date': 1662854400000, 'Close':20652.5},
      //         {'Date': 1662940800000, 'Close':20252.5},
      //       ],
      //     'sentiment': [
      //         {'Date': 1662681600000, 'Sentiment':0.3},
      //         {'Date': 1662768000000, 'Sentiment':0.7},
      //         {'Date': 1662854400000, 'Sentiment':0.5},
      //         {'Date': 1662940800000, 'Sentiment':0.1},
      //     ]
      //   }

      let path = "http://localhost:5000/getTimeSeriesData";
      try {
        const response = await axios.post(path, {
          params: {
            asset_name: 'AAPL'
          },
        });

        vm.plotData = response.data
        console.log(vm.plotData)

      } catch (error) {
        // pop up the error message
        console.log(error.message)
      }
    },
    
    async loadParameterData() {
      let vm = this;      
      let path = "http://localhost:5000/getParameters";
      try {
        const response = await axios.post(path, {
          params: {
            asset_name: 'AAPL'
          },
        });

        vm.parameterData = response.data

      } catch (error) {
        // pop up the error message
        console.log(error.message)
      }
    },

    async loadAssetData() {
      let vm = this;      
      let path = "http://localhost:5000/getAsset";
      try {
        const response = await axios.post(path, {
          params: {
            asset_name: 'AAPL'
          },
        });

        vm.assetData = response.data
      } catch (error) {
        // pop up the error message
        console.log(error.message)
      }
    },

    async loadIndicatorData() {
      let vm = this;      
      let path = "http://localhost:5000/getIndicator";
      try {
        const response = await axios.post(path, {
          params: {
            asset_name: 'AAPL'
          },
        });

        vm.indicatorData = response.data
      } catch (error) {
        // pop up the error message
        console.log(error.message)
      }
    }
  },

  async beforeMount() {
    let vm = this;

    await vm.loadAssetData()
    await vm.loadIndicatorData()

    await vm.loadPlotData()
    await vm.loadData()  
    await vm.loadUserData()    

    await vm.loadParameterData()
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
  margin: 3px;
}

.span-table-title {
  font-weight: bold;
}

.div-container {
  margin: 10px;
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