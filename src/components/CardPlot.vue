<template>
    <div class="row">
        <div v-for="d in listData" :key="d.value" class="box-card col-6">
            <el-card>
                <span style="font-size: 15pt; font-weight:bold">{{ d.value }}</span>
                <br>
                <span style="font-size: 9pt">{{ d.name }}</span>
            </el-card>
        </div>
    </div>

</template>

<script>
export default {
  name: 'TablePlot',
  props: {
    listData: {
      type: Array,
      default: () => {
        return [
            {'name':'parameter1', 'value': '123M'},
            {'name':'parameter2', 'value': '123M'},
            {'name':'parameter3', 'value': '123M'},
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
.box-card {
    min-width: 80px;
    display: inline;
    margin-bottom: 10px;
}
</style>

