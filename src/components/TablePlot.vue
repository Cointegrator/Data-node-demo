<template>
    <div>
        <el-table 
          stripe border highlight-current-row style="width: 100%" 
          header-row-class-name="table-header"
          :header-cell-style="{ background: 'rgb(217, 217, 217)', border: 'gray solid .5px' }"
          :data="pagedTableData">
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
export default {
  name: 'TablePlot',
  props: {
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
      pageSize: 13,
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
        if (value.length > 13) {
          return value.slice(0, 13);
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

