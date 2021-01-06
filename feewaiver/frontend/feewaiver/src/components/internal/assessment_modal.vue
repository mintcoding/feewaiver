<template lang="html">
    <div id="AssessmentWorkflow">
        <modal transition="modal fade" @ok="ok()" @cancel="cancel()" :title="modalTitle" large force>
          <div class="container-fluid">
            <div class="row">
                <div class="col-sm-12">
                        <div class="form-group">
                          <div class="row">
                              <div class="col-sm-3">
                                  <label class="control-label pull-left" for="details">Details</label>
                              </div>
            			      <div class="col-sm-6">
			                	  <!--textarea v-if="workflow_type === 'close'" class="form-control" placeholder="add details" id="details" v-model="advice_details"/-->
                                  <textarea class="form-control" placeholder="add details" id="details" v-model="workflowDetails"/>
                              </div>
                          </div>
                        </div>
                        <div class="form-group">
                            <div class="row">
                                <div class="col-sm-3">
                                    <label class="control-label pull-left"  for="Name">Attachments</label>
                                </div>
            			        <div class="col-sm-9">
                                    <FileField ref="comms_log_file" name="comms-log-file" :isRepeatable="true" :documentActionUrl="documentActionUrl"  />
                                </div>
                            </div>
                        </div>

                </div>
              
            </div>
          </div>
            <div slot="footer">
                <div v-if="errorResponse" class="form-group">
                    <div class="row">
                        <div class="col-sm-12">
                            <strong>
                                <span style="white-space: pre;">{{ errorResponse }}</span>
                            </strong>
                        </div>
                    </div>
                </div>
                <!--button type="button" class="btn btn-default" @click="ok">Ok</button>
                <button type="button" class="btn btn-default" @click="cancel">Cancel</button-->
                <div v-if="processingWorkflow">
                    <button type="button" disabled class="btn btn-default" @click="ok"><i class="fa fa-spinner fa-spin"></i> Processing</button>
                    <!--span v-else-if="ok_button_disabled" class="d-inline-block" tabindex="0" data-toggle="tooltip" title="Please select at least one site to issue">
                        <button type="button" style="pointer-events: none;" class="btn btn-default" @click="ok" disabled>Ok</button>
                    </span-->
                </div>
                <div v-else>
                    <button type="button" class="btn btn-default" @click="ok" >Ok</button>
                    <button type="button" class="btn btn-default" @click="cancel">Cancel</button>
                </div>
            </div>
        </modal>
    </div>
</template>
<script>
import Vue from "vue";
import modal from '@vue-utils/bootstrap-modal.vue';
//import { mapState, mapGetters, mapActions, mapMutations } from "vuex";
import { api_endpoints, helpers, cache_helper } from "@/utils/hooks";
//import filefield from '@/components/common/compliance_file.vue';
require("select2/dist/css/select2.min.css");
require("select2-bootstrap-theme/dist/select2-bootstrap.min.css");
//import { required, minLength, between } from 'vuelidate/lib/validators'
import FileField from '@/components/forms/filefield_immediate.vue'

export default {
    name: "AssessmentWorkflow",
    data: function() {
      return {
            //officers: [],
            isModalOpen: false,
            /*
            processingDetails: false,
            form: null,
            regions: [],
            regionDistricts: [],
            availableDistricts: [],
            externalOrganisations: [],
            referrers: [],
            referrersSelected: [],
            */
            workflowDetails: "",
            errorResponse: "",
            modalTitle: "",
            processingWorkflow: false,
            /*
            region_id: null,
            district_id: null,
            assigned_to_id: null,
            inspection_type_id: null,
            case_priority_id: null,
            advice_details: "",
            allocatedGroup: [],
            allocated_group_id: null,
            files: [
                    {
                        'file': null,
                        'name': ''
                    }
                ]
            */
      }
    },
    components: {
      modal,
      FileField,
    },
    props:{
          workflow_type: {
              type: String,
              default: '',
          },
          feeWaiver: {
              type: Object,
              required: true,
          },
      },
    computed: {
        documentActionUrl: function() {
            return `/api/feewaivers/${this.feeWaiver.id}/process_comms_log_document/`;
        },
    },
    filters: {
      formatDate: function(data) {
          return data ? moment(data).format("DD/MM/YYYY HH:mm:ss") : "";
      }
    },
    methods: {
      setModalTitle: function() {
          if (this.workflow_type === 'propose_issue') {
              this.modalTitle = 'Propose Issue';
          } else if (this.workflow_type === 'propose_concession') {
              this.modalTitle = 'Propose Concession';
          } else if (this.workflow_type === 'propose_decline') {
              this.modalTitle = 'Propose Decline';
          } else if (this.workflow_type === 'issue') {
              this.modalTitle = 'Issue';
          } else if (this.workflow_type === 'issue_concession') {
              this.modalTitle = 'Issue Concession';
          } else if (this.workflow_type === 'decline') {
              this.modalTitle = 'Decline';
          } else if (this.workflow_type === 'return_to_assessor') {
              this.modalTitle = 'Return to Assessor';
          }
      },

        /*
      ok: async function () {
          const response = await this.sendData();
          console.log(response);
          if (response === 'ok') {
              this.close();
          }
      },
      */
      cancel: async function() {
          await this.$refs.comms_log_file.cancel();
          //this.isModalOpen = false;
          this.close();
      },
      close: function () {
          //let vm = this;
          this.$parent.workflowActionType = '';
          this.isModalOpen = false;
      },
      //sendData: async function(){        
      ok: async function(){        
          this.processingWorkflow = true;
          let post_url = '/api/feewaivers/' + this.feeWaiver.id + '/workflow_action/'
          let payload = new FormData(this.form);
          
          this.workflowDetails ? payload.append('comments', this.workflowDetails) : null;
          //this.advice_details ? payload.append('advice_details', this.advice_details) : null;
          this.$refs.comms_log_file.commsLogId ? payload.append('comms_log_id', this.$refs.comms_log_file.commsLogId) : null;
          this.workflow_type ? payload.append('workflow_type', this.workflow_type) : null;
          this.modalTitle ? payload.append('email_subject', this.modalTitle) : null;
          /*
          this.referrersSelected ? payload.append('referrers_selected', this.referrersSelected) : null;
          this.district_id ? payload.append('district_id', this.district_id) : null;
          this.assigned_to_id ? payload.append('assigned_to_id', this.assigned_to_id) : null;
          this.inspection_type_id ? payload.append('inspection_type_id', this.inspection_type_id) : null;
          this.case_priority_id ? payload.append('case_priority_id', this.case_priority_id) : null;
          this.region_id ? payload.append('region_id', this.region_id) : null;
          this.allocated_group_id ? payload.append('allocated_group_id', this.allocated_group_id) : null;
          */

          //let callEmailRes = await this.saveCallEmail({ crud: 'save', 'internal': true });
          //let feeWaiverRes = await this.$http.post(url, payload)
            //this.$refs.fee_waiver_form.save(false);
            //this.$http.post(`/api/feewaivers/${this.feeWaiverId}/workflow_action/`, {"action": action})
          let feeWaiverRes = await this.$parent.parentSave(false)
          console.log(feeWaiverRes);
          if (feeWaiverRes.ok) {
              try {
                  let res = await Vue.http.post(post_url, payload);
                  if (res.ok) {    
                      this.$router.push({
                          name: 'fee-waiver-dash',
                      });
                      //this.$router.push({ name: 'internal-call-email-dash' });
                  }
              } catch(err) {
                  this.errorResponse = 'Error:' + err.statusText;
              } 
          } else {
              this.errorResponse = 'Error:' + feeWaiverRes.statusText;
          }
          this.processingWorkflow = false;
      },
      /*
      uploadFile(target,file_obj){
          let vm = this;
          let _file = null;
          var file_input = $('.'+target)[0];

          if (file_input.files && file_input.files[0]) {
              var reader = new FileReader();
              reader.readAsDataURL(file_input.files[0]); 
              reader.onload = function(e) {
                  _file = e.target.result;
              };
              _file = file_input.files[0];
          }
          file_obj.file = _file;
          file_obj.name = _file.name;
      },
      removeFile(index){
          let length = this.files.length;
          $('.file-row-'+index).remove();
          this.files.splice(index,1);
          this.$nextTick(() => {
              length == 1 ? this.attachAnother() : '';
          });
      },
      attachAnother(){
          this.files.push({
              'file': null,
              'name': ''
          })
      },
      */
    },
    created: async function() {
    },
    mounted: function() {
        //this.form = document.forms.forwardForm;
        this.$nextTick(() => {
            this.setModalTitle();
        });
    }
};
</script>

<style lang="css">
/*
.btn-file {
    position: relative;
    overflow: hidden;
}
.btn-file input[type=file] {
    position: absolute;
    top: 0;
    right: 0;
    min-width: 100%;
    min-height: 100%;
    font-size: 100px;
    text-align: right;
    filter: alpha(opacity=0);
    opacity: 0;
    outline: none;
    background: white;
    cursor: inherit;
    display: block;
}
*/
.top-buffer{margin-top: 5px;}
.top-buffer-2x{margin-top: 10px;}
</style>
