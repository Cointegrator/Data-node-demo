<template>
    <div>
        <el-table 
          border highlight-current-row style="width: 100%" 
          header-row-class-name="table-header"
          :header-cell-style="{ background: 'rgb(217, 217, 217)', border: 'gray solid .5px' }"
          :data="pagedTableData"
          @row-click="handleRowClick"
          @row-mouseenter="handleRowMouseEnter">
            <el-table-column
            sortable
            v-for="column in tableColumns"
            :key="column.label"
            :min-width="column.minWidth"
            :prop="column.prop"
            :label="column.label"
            :formatter="formatTableData"
            >
            </el-table-column>
        </el-table>
        <el-pagination
          layout="prev, pager, next"
          :total="this.tableData.length"
          @current-change="setPage"
        >
        </el-pagination>
    </div>

</template>

<script>
import { bus } from "../main"
export default {
  name: 'TablePlot',
  props: {
    charLength: {
      type: Number,
      default: () => {
        return 12;
      }
    },
    tableName: {
      type: String,
      default: () => {
        return "defaultTableName";
      }
    },
    tableColumns: {
      type: Array,
      default: () => {
        return [
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
        ]
      }
    },
    tableData: {
      type: Array,
      default: () => {
        return [
            {'asset_name':'AAPL', 'feature_0':123, 'feature_1':23},
            {'asset_name':'TSLA', 'feature_0':13, 'feature_1':23},
            {'asset_name':'GOOG', 'feature_0':113, 'feature_1':2}
        ];
      },
    },
  },
  components: {
  },
  data() {
    return {
      page: 1,
      pageSize: 10,
    }
  },
  computed: {
    pagedTableData() {
      return this.tableData.slice(
        this.pageSize * this.page - this.pageSize,
        this.pageSize * this.page
      );
    },
  },
  methods: {
    handleRowClick(row, event, column) {
      // 'row' contains the data of the clicked row
      // 'event' is the click event
      // 'column' is the column component where the click occurred
      // console.log('Clicked row data:', row);
      // console.log('Click event:', event);
      // console.log('Clicked column:', column);

      if(this.tableName==='assetTable') {
        bus.$emit('change_selected_asset', row['name']) 
      }
      if(this.tableName==='indicatorTable') {
        console.log(row['Description'])
      }
    },
    handleRowMouseEnter(row, event, column) {
      console.log(row)
      if(this.tableName==='indicatorTable') {
        console.log(row)
      }
    },
    setPage(val) {
      this.page = val;
    },
    isFloat(value) {
      return typeof value === 'number' && !Number.isInteger(value);
    },
    formatTableData(row, col, value, index) {
      let vm = this;
      if(vm.isFloat(value)) {
        return value.toFixed(3)
      }
      else if(typeof value === 'string') {
        if (value.length > vm.charLength) {
          return value.slice(0, vm.charLength);
        }
        else {
          return value;
        }
      }
      else if (value instanceof Date) {
        return value.toLocaleString();
      } else {
        return value;
      }
    },
  },
  async beforeMount() {

  },
  mounted() {},
}
</script>


<style scoped>

</style>

