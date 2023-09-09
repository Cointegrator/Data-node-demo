<template>
    <div>
        <el-table stripe style="width: 100%" :data="tableData" border>
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
    }
  },
  methods: {
  },
  async beforeMount() {

  },
  mounted() {},
}
</script>


<style scoped>

</style>

