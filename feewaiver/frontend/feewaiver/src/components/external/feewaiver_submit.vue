<template lang="html">
    <div class="container" >
        <div class="row">
            <div class="col-sm-12">
                <div class="row">
                    <div v-if="feeWaiver && feeWaiver.id" class="col-sm-offset-3 col-sm-6 borderDecoration">
                        <strong>Your Entry Fee Waiver Request form has been successfully submitted.</strong>
                        <br/>
                        <table>
                            <tr>
                                <td><strong>Entry Fee Waiver Request:</strong></td>
                                <td><strong>{{feeWaiver.lodgement_number}}</strong></td>
                            </tr>
                            <tr>
                                <td><strong>Date/Time:</strong></td>
                                <td><strong> {{feeWaiver.lodgement_date|formatDate}}</strong></td>
                            </tr>
                        </table>
                        <router-link :to="{name:'external-feewaiver-form'}" style="margin-top:15px;" class="btn btn-primary">Lodge another request</router-link>
                    </div>
                    <div v-else class="col-sm-offset-3 col-sm-6 borderDecoration">
                        <strong>Sorry, it looks like there is no Fee Waiver currently in your session.</strong>
                        <br /><router-link :to="{name:'external-feewaiver-form'}" style="margin-top:15px;" class="btn btn-primary">Return to form</router-link>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import Vue from 'vue'
import {
  api_endpoints,
  helpers
}
from '@/utils/hooks'
//import utils from './utils'
export default {
  data: function() {
    let vm = this;
    return {
        "feeWaiver": {},
    }
  },
  components: {
  },
  computed: {
  },
  methods: {
  },
  filters:{
        formatDate: function(data){
            return data ? moment(data).format('DD/MM/YYYY HH:mm:ss'): '';
        }
  },
  mounted: function() {
      this.$nextTick(() => {
          if (!Object.keys(this.feeWaiver).length) {
              this.$router.push({
                  name: 'external-feewaiver-form',
              });
          }
      });
  },
  beforeRouteEnter: function(to, from, next) {
    next(vm => {
        vm.feeWaiver = Object.assign({}, to.params.fee_waiver);
    })
  }
}
</script>

<style lang="css" scoped>
.borderDecoration {
    border: 1px solid;
    border-radius: 5px;
    padding: 50px;
    margin-top: 70px;
}
</style>
