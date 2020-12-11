<template lang="html">
    <div v-if="feeWaiver" class="container" id="internalAssessment">
      <div class="row">
        <h3>Entry Fee Waiver Request: {{ feeWaiver.lodgement_number }}</h3>
        <div class="col-md-3">
            <CommsLogs :comms_url="comms_url" :logs_url="logs_url" :comms_add_url="comms_add_url" :disable_add_entry="false"/>

            <div class="row">
                <div class="panel panel-default">
                    <div class="panel-heading">
                        Workflow
                    </div>
                    <div class="panel-body panel-collapse">
                        <div class="row">
                            <div class="col-sm-12">
                                <strong>Status</strong><br/>
                                {{ feeWaiver.processing_status }}
                            </div>
                            <div class="col-sm-12">
                                <div class="separator"></div>
                            </div>

                            <div class="col-sm-12 top-buffer-s">
                                <strong>Currently assigned to</strong><br/>
                                <div class="form-group">
                                    <!--template v-if="feeWaiver.processing_status == 'With Approver'"-->
                                    <template>
                                        <select ref="assigned_officer" :disabled="!canAction" class="form-control" v-model="feeWaiver.assigned_officer_id">
                                            <option :value="null"></option>
                                            <option v-for="member in feeWaiver.action_group" :value="member.id">{{member.first_name}} {{member.last_name}}</option>
                                        </select>
                                        <a v-if="canAssess && feeWaiver.assigned_officer != feeWaiver.current_officer.id" @click.prevent="assignRequestUser()" class="actionBtn pull-right">Assign to me</a>
                                    </template>
                                </div>
                            </div>

                            <div class="col-sm-12 top-buffer-s" v-if="!isFinalised && canAction">
                                <template v-if="feeWaiver.processing_status == 'With Assessor'">
                                    <div class="row">
                                        <div class="col-sm-12">
                                            <strong>Action</strong><br/>
                                        </div>
                                    </div>
                                    <div class="row">
                                        <div class="col-sm-12">
                                            <button style="width:80%;" class="btn btn-primary" :disabled="false" @click.prevent="switchStatus('with_assessor')">Propose Issue Fee Waiver</button><br/>
                                        </div>
                                    </div>
                                    <div class="row">
                                        <div class="col-sm-12">
                                            <button style="width:80%;" class="btn btn-primary top-buffer-s" :disabled="false" @click.prevent="proposedApproval()">Propose</button><br/>
                                        </div>
                                    </div>
                                </template>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-md-1"></div>
        <div class="col-md-8">
            <div class="row">
                <FeeWaiverForm 
                :feeWaiverId="feeWaiverId"
                :key="feeWaiverId"/>
            </div>
        </div>
        </div>
        <!--ProposedDecline ref="proposed_decline" :processing_status="feeWaiver.processing_status" :feeWaiver_id="feeWaiver.id" @refreshFromResponse="refreshFromResponse"></ProposedDecline>
        <AmendmentRequest 
        ref="amendment_request" 
        :feeWaiver_id="feeWaiver.id" 
        :is_apiary_feeWaiver="isApiaryProposal"
        @refreshFromResponse="refreshFromResponse"
        />
        <ProposedApiaryIssuance 
            ref="proposed_approval" 
            :processing_status="feeWaiver.processing_status" 
            :feeWaiver_apiary_id="apiaryProposal.id" 
            :feeWaiver_id="feeWaiverId" 
            :feeWaiver="feeWaiver"
            :feeWaiver_type='feeWaiver.feeWaiver_type' 
            :isApprovalLevelDocument="isApprovalLevelDocument" 
            :submitter_email="feeWaiver.submitter_email" 
            :applicant_email="applicant_email" 
            @refreshFromResponse="refreshFromResponse"
        /-->
    </div>
</template>
<script>
import CommsLogs from '@common-utils/comms_logs.vue'
import { api_endpoints, helpers } from '@/utils/hooks'
import FeeWaiverForm from '../feewaiver_form.vue'
import Vue from 'vue'


export default {
    name: 'Assessment',
    data: function() {
        let vm = this;
        return {
            feeWaiverId: null,
            feeWaiver: {},
            detailsBody: 'detailsBody'+vm._uid,
            addressBody: 'addressBody'+vm._uid,
            contactsBody: 'contactsBody'+vm._uid,
            siteLocations: 'siteLocations'+vm._uid,
            defaultKey: "aho",
            "feeWaiver": null,
            "original_feeWaiver": null,
            "loading": [],
            selected_referral: '',
            referral_text: '',
            approver_comment: '',
            form: null,
            members: [],
            //department_users : [],
            apiaryReferralGroups: [],
            contacts_table_initialised: false,
            initialisedSelects: false,
            showingProposal:false,
            showingRequirements:false,
            hasAmendmentRequest: false,
            DATE_TIME_FORMAT: 'DD/MM/YYYY HH:mm:ss',
            comms_url: helpers.add_endpoint_json('/api/feewaivers',vm.$route.params.fee_waiver_id+'/comms_log'),
            comms_add_url: helpers.add_endpoint_json('/api/feewaivers',vm.$route.params.fee_waiver_id+'/add_comms_log'),
            logs_url: helpers.add_endpoint_json('/api/feewaivers',vm.$route.params.fee_waiver_id+'/action_log'),
            panelClickersInitialised: false,
            //is_local: helpers.is_local(),
        }
    },
    components: {
        CommsLogs,
        FeeWaiverForm,
    },
    filters: {
        formatDate: function(data){
            return data ? moment(data).format('DD/MM/YYYY HH:mm:ss'): '';
        }
    },
    props: {
        /*
        feeWaiverId: {
            type: Number,
        },
        */
    },
    watch: {

    },
    computed: {
        feeWaiver_form_url: function() {
            /*
            if (this.apiaryProposal) {
                return `/api/feeWaiver_apiary/${this.apiaryProposal.id}/assessor_save.json`;
            }
            */
        },
        isFinalised: function(){
            return this.feeWaiver.processing_status == 'Declined' || this.feeWaiver.processing_status == 'Approved';
        },
        canAssess: function() {
            return true;
        },
        /*
        canAssess: function(){
            return this.feeWaiver && this.feeWaiver.assessor_mode.assessor_can_assess ? true : false;
        },
        */
        canAction: function() {
            return true;
        },
        /*
        hasAssessorMode:function(){
            return this.feeWaiver && this.feeWaiver.assessor_mode.has_assessor_mode ? true : false;
        },
        canAction: function(){
            if (this.feeWaiver.processing_status == 'With Approver'){
                return this.feeWaiver && (this.feeWaiver.processing_status == 'With Approver' || this.feeWaiver.processing_status == 'With Assessor' || this.feeWaiver.processing_status == 'With Assessor (Requirements)') && !this.isFinalised && !this.feeWaiver.can_user_edit && (this.feeWaiver.current_assessor.id == this.feeWaiver.assigned_approver || this.feeWaiver.assigned_approver == null ) && this.feeWaiver.assessor_mode.assessor_can_assess? true : false;
            }
            else{
                return this.feeWaiver && (this.feeWaiver.processing_status == 'With Approver' || this.feeWaiver.processing_status == 'With Assessor' || this.feeWaiver.processing_status == 'With Assessor (Requirements)') && !this.isFinalised && !this.feeWaiver.can_user_edit && (this.feeWaiver.current_assessor.id == this.feeWaiver.assigned_officer || this.feeWaiver.assigned_officer == null ) && this.feeWaiver.assessor_mode.assessor_can_assess? true : false;
            }
        },
        canLimitedAction: function(){
            if (this.feeWaiver.processing_status == 'With Approver'){
                return this.feeWaiver && (this.feeWaiver.processing_status == 'With Assessor' || this.feeWaiver.processing_status == 'With Referral' || this.feeWaiver.processing_status == 'With Assessor (Requirements)') && !this.isFinalised && !this.feeWaiver.can_user_edit && (this.feeWaiver.current_assessor.id == this.feeWaiver.assigned_approver || this.feeWaiver.assigned_approver == null ) && this.feeWaiver.assessor_mode.assessor_can_assess? true : false;
            }
            else{
                return this.feeWaiver && (this.feeWaiver.processing_status == 'With Assessor' || this.feeWaiver.processing_status == 'With Referral' || this.feeWaiver.processing_status == 'With Assessor (Requirements)') && !this.isFinalised && !this.feeWaiver.can_user_edit && (this.feeWaiver.current_assessor.id == this.feeWaiver.assigned_officer || this.feeWaiver.assigned_officer == null ) && this.feeWaiver.assessor_mode.assessor_can_assess? true : false;
            }
        },
        */
    },
    methods: {
        commaToNewline(s){
            return s.replace(/[,;]/g, '\n');
        },
        proposedDecline: function(){
            this.save_wo();
            this.$refs.proposed_decline.decline = this.feeWaiver.feeWaiverdeclineddetails != null ? helpers.copyObject(this.feeWaiver.feeWaiverdeclineddetails): {};
            this.$refs.proposed_decline.isModalOpen = true;
        },
        proposedApproval: function(){
            let copiedProposedIssuanceApproval = helpers.copyObject(this.feeWaiver.proposed_issuance_approval);
            if (this.feeWaiver.feeWaiver_type == 'Renewal') {
                copiedProposedIssuanceApproval.expiry_date = null;
            }
            this.$refs.proposed_approval.approval = this.feeWaiver.proposed_issuance_approval != null ? copiedProposedIssuanceApproval : {};
            if(this.feeWaiver.proposed_issuance_approval == null){
                var test_approval={
                'cc_email': this.feeWaiver.referral_email_list
            };
            this.$refs.proposed_approval.approval=helpers.copyObject(test_approval);
                // this.$refs.proposed_approval.$refs.bcc_email=this.feeWaiver.referral_email_list;
            }
            //this.$refs.proposed_approval.submitter_email=helpers.copyObject(this.feeWaiver.submitter_email);
            // if(this.feeWaiver.applicant.email){
            //     this.$refs.proposed_approval.applicant_email=helpers.copyObject(this.feeWaiver.applicant.email);
            // }
            this.$refs.proposed_approval.isModalOpen = true;
            // Force to refresh the map to display it in case it is not shown.  
            // When the map is in modal, it is often not shown unless the map is resized
            this.$refs.proposed_approval.forceToRefreshMap()
        },
        issueProposal:function(){
            //this.$refs.proposed_approval.approval = helpers.copyObject(this.feeWaiver.proposed_issuance_approval);
            console.log('in issueProposal')
            //save approval level comment before opening 'issue approval' modal
            if(this.feeWaiver && this.feeWaiver.processing_status == 'With Approver' && this.feeWaiver.approval_level != null && this.feeWaiver.approval_level_document == null){
                if (this.feeWaiver.approval_level_comment!='')
                {
                    let vm = this;
                    let data = new FormData();
                    data.append('approval_level_comment', vm.feeWaiver.approval_level_comment)
                    vm.$http.post(helpers.add_endpoint_json(api_endpoints.feeWaivers,vm.feeWaiver.id+'/approval_level_comment'),data,{
                        emulateJSON:true
                        }).then(res=>{
                        vm.feeWaiver = res.body;
                    vm.refreshFromResponse(res);
                    },err=>{
                    console.log(err);
                    });
                }
            }
            if(this.isApprovalLevelDocument && this.feeWaiver.approval_level_comment=='')
            {
                swal(
                    'Error',
                    'Please add Approval document or comments before final approval',
                    'error'
                )
            }
            else{
                this.$refs.proposed_approval.approval = this.feeWaiver.proposed_issuance_approval != null ? helpers.copyObject(this.feeWaiver.proposed_issuance_approval) : {};
                this.$refs.proposed_approval.state = 'final_approval';
                this.$refs.proposed_approval.isApprovalLevelDocument = this.isApprovalLevelDocument;
                //this.$refs.proposed_approval.submitter_email=helpers.copyObject(this.feeWaiver.submitter_email);
                // if(this.feeWaiver.applicant.email){
                //     this.$refs.proposed_approval.applicant_email=helpers.copyObject(this.feeWaiver.applicant.email);
                // }
                this.$refs.proposed_approval.isModalOpen = true;

                // Force to refresh the map to display it in case it is not shown.  
                // When the map is in modal, it is often not shown unless the map is resized
                this.$refs.proposed_approval.forceToRefreshMap()
            }
        },
        declineProposal:function(){
            this.$refs.proposed_decline.decline = this.feeWaiver.feeWaiverdeclineddetails != null ? helpers.copyObject(this.feeWaiver.feeWaiverdeclineddetails): {};
            this.$refs.proposed_decline.isModalOpen = true;
        },
        amendmentRequest: function(){
            this.save_wo();
            let values = '';
            $('.deficiency').each((i,d) => {
                values +=  $(d).val() != '' ? `Question - ${$(d).data('question')}\nDeficiency - ${$(d).val()}\n\n`: '';
            });
            //this.deficientFields();
            this.$refs.amendment_request.amendment.text = values;

            this.$refs.amendment_request.isModalOpen = true;
        },
        highlight_deficient_fields: function(deficient_fields){
            let vm = this;
            for (var deficient_field of deficient_fields) {
                $("#" + "id_"+deficient_field).css("color", 'red');
            }
        },
        deficientFields(){
            let vm=this;
            let deficient_fields=[]
            $('.deficiency').each((i,d) => {
                if($(d).val() != ''){
                    var name=$(d)[0].name
                    var tmp=name.replace("-comment-field","")
                    deficient_fields.push(tmp);
                    //console.log('data', $("#"+"id_" + tmp))
                }
            });
            //console.log('deficient fields', deficient_fields);
            vm.highlight_deficient_fields(deficient_fields);
        },
        save: function(e) {
          let vm = this;
          vm.checkAssessorData();
          let formData = new FormData(vm.form);
          vm.$http.post(vm.feeWaiver_form_url,formData).then(res=>{
              swal(
                'Saved',
                'Your feeWaiver has been saved',
                'success'
              )
          },err=>{
          });
        },
        save_wo: function() {
          let vm = this;
          vm.checkAssessorData();
          let formData = new FormData(vm.form);
          vm.$http.post(vm.feeWaiver_form_url,formData).then(res=>{


          },err=>{
          });
        },

        updateAssignedOfficerSelect:function(){
            let vm = this;
            /*
            if (vm.feeWaiver.processing_status == 'With Approver'){
                $(vm.$refs.assigned_officer).val(vm.feeWaiver.assigned_approver);
                $(vm.$refs.assigned_officer).trigger('change');
            }
            else{
                $(vm.$refs.assigned_officer).val(vm.feeWaiver.assigned_officer);
                $(vm.$refs.assigned_officer).trigger('change');
            }
            */
            $(vm.$refs.assigned_officer).val(vm.feeWaiver.assigned_officer);
            $(vm.$refs.assigned_officer).trigger('change');
        },
        assignRequestUser: function(){
            let vm = this;
            vm.$http.get(helpers.add_endpoint_json('/api/feewaivers',(vm.feeWaiver.id+'/assign_request_user')))
            .then((response) => {
                vm.feeWaiver = response.body;
                /*
                vm.original_feeWaiver = helpers.copyObject(response.body);
                vm.feeWaiver.applicant.address = vm.feeWaiver.applicant.address != null ? vm.feeWaiver.applicant.address : {};
                */
                vm.updateAssignedOfficerSelect();
            }, (error) => {
                /*
                vm.feeWaiver = helpers.copyObject(vm.original_feeWaiver)
                vm.feeWaiver.applicant.address = vm.feeWaiver.applicant.address != null ? vm.feeWaiver.applicant.address : {};
                */
                vm.updateAssignedOfficerSelect();
                swal(
                    'Proposal Error',
                    helpers.apiVueResourceError(error),
                    'error'
                )
            });
        },
        /*
        refreshFromResponse:function(response){
            let vm = this;
            vm.original_feeWaiver = helpers.copyObject(response.body);
            vm.feeWaiver = helpers.copyObject(response.body);
            vm.feeWaiver.applicant.address = vm.feeWaiver.applicant.address != null ? vm.feeWaiver.applicant.address : {};
            vm.$nextTick(() => {
                vm.initialiseAssignedOfficerSelect(true);
                vm.updateAssignedOfficerSelect();
            });
            if (vm.$refs.approval_screen){
                vm.$refs.approval_screen.updateComponentSiteSelectionKey()
            }
        },
        */
        assignTo: function(){
            let vm = this;
            let unassign = true;
            let data = {};
            /*
            if (vm.processing_status == 'With Approver'){
                unassign = vm.feeWaiver.assigned_approver != null && vm.feeWaiver.assigned_approver != 'undefined' ? false: true;
                data = {'assessor_id': vm.feeWaiver.assigned_approver};
            }
            else{
                unassign = vm.feeWaiver.assigned_officer != null && vm.feeWaiver.assigned_officer != 'undefined' ? false: true;
                data = {'assessor_id': vm.feeWaiver.assigned_officer};
            }
            */
            unassign = vm.feeWaiver.assigned_officer != null ? false: true;
            data = {'assigned_officer_id': vm.feeWaiver.assigned_officer};
            if (!unassign){
                vm.$http.post(helpers.add_endpoint_json('/api/feewaivers',(vm.feeWaiver.id+'/assign_to')),JSON.stringify(data),{
                    emulateJSON:true
                }).then((response) => {
                    vm.feeWaiver = response.body;
                    /*
                    vm.original_feeWaiver = helpers.copyObject(response.body);
                    vm.feeWaiver.applicant.address = vm.feeWaiver.applicant.address != null ? vm.feeWaiver.applicant.address : {};
                    */
                    vm.updateAssignedOfficerSelect();
                }, (error) => {
                    /*
                    vm.feeWaiver = helpers.copyObject(vm.original_feeWaiver)
                    vm.feeWaiver.applicant.address = vm.feeWaiver.applicant.address != null ? vm.feeWaiver.applicant.address : {};
                    */
                    vm.updateAssignedOfficerSelect();
                    swal(
                        'Proposal Error',
                        helpers.apiVueResourceError(error),
                        'error'
                    )
                });
            }
            else{
                vm.$http.get(helpers.add_endpoint_json('/api/feewaivers',(vm.feeWaiver.id+'/unassign')))
                .then((response) => {
                    vm.feeWaiver = response.body;
                    /*
                    vm.original_feeWaiver = helpers.copyObject(response.body);
                    vm.feeWaiver.applicant.address = vm.feeWaiver.applicant.address != null ? vm.feeWaiver.applicant.address : {};
                    */
                    vm.updateAssignedOfficerSelect();
                }, (error) => {
                    /*
                    vm.feeWaiver = helpers.copyObject(vm.original_feeWaiver)
                    vm.feeWaiver.applicant.address = vm.feeWaiver.applicant.address != null ? vm.feeWaiver.applicant.address : {};
                    */
                    vm.updateAssignedOfficerSelect();
                    swal(
                        'Proposal Error',
                        helpers.apiVueResourceError(error),
                        'error'
                    )
                });
            }
        },
        switchStatus: function(status){
            let vm = this;
            //vm.save_wo();
            //let vm = this;
            if(vm.feeWaiver.processing_status == 'With Assessor' && status == 'with_assessor_requirements'){
            vm.checkAssessorData();
            let formData = new FormData(vm.form);
            vm.$http.post(vm.feeWaiver_form_url,formData).then(res=>{ //save Proposal before changing status so that unsaved assessor data is saved.

            let data = {'status': status, 'approver_comment': vm.approver_comment}
            vm.$http.post(helpers.add_endpoint_json(api_endpoints.feeWaivers,(vm.feeWaiver.id+'/switch_status')),JSON.stringify(data),{
                emulateJSON:true,
            })
            .then((response) => {
                vm.feeWaiver = response.body;
                vm.original_feeWaiver = helpers.copyObject(response.body);
                vm.feeWaiver.applicant.address = vm.feeWaiver.applicant.address != null ? vm.feeWaiver.applicant.address : {};
                vm.approver_comment='';
                vm.$nextTick(() => {
                    vm.initialiseAssignedOfficerSelect(true);
                    vm.updateAssignedOfficerSelect();
                });

            }, (error) => {
                vm.feeWaiver = helpers.copyObject(vm.original_feeWaiver)
                vm.feeWaiver.applicant.address = vm.feeWaiver.applicant.address != null ? vm.feeWaiver.applicant.address : {};
                swal(
                    'Proposal Error',
                    helpers.apiVueResourceError(error),
                    'error'
                )
            });

          },err=>{
          });
        }

        //if approver is pushing back feeWaiver to Assessor then navigate the approver back to dashboard page
        if(vm.feeWaiver.processing_status == 'With Approver' && (status == 'with_assessor_requirements' || status=='with_assessor')) {
            let data = {'status': status, 'approver_comment': vm.approver_comment}
            vm.$http.post(helpers.add_endpoint_json(api_endpoints.feeWaivers,(vm.feeWaiver.id+'/switch_status')),JSON.stringify(data),{
                emulateJSON:true,
            })
            .then((response) => {
                vm.feeWaiver = response.body;
                vm.original_feeWaiver = helpers.copyObject(response.body);
                vm.feeWaiver.applicant.address = vm.feeWaiver.applicant.address != null ? vm.feeWaiver.applicant.address : {};
                vm.approver_comment='';
                vm.$nextTick(() => {
                    vm.initialiseAssignedOfficerSelect(true);
                    vm.updateAssignedOfficerSelect();
                });
                vm.$router.push({ path: '/internal' });
            }, (error) => {
                vm.feeWaiver = helpers.copyObject(vm.original_feeWaiver)
                vm.feeWaiver.applicant.address = vm.feeWaiver.applicant.address != null ? vm.feeWaiver.applicant.address : {};
                swal(
                    'Proposal Error',
                    helpers.apiVueResourceError(error),
                    'error'
                )
            });

        }

        else{


         let data = {'status': status, 'approver_comment': vm.approver_comment}
            vm.$http.post(helpers.add_endpoint_json(api_endpoints.feeWaivers,(vm.feeWaiver.id+'/switch_status')),JSON.stringify(data),{
                emulateJSON:true,
            })
            .then((response) => {
                vm.feeWaiver = response.body;
                vm.original_feeWaiver = helpers.copyObject(response.body);
                vm.feeWaiver.applicant.address = vm.feeWaiver.applicant.address != null ? vm.feeWaiver.applicant.address : {};
                vm.approver_comment='';
                vm.$nextTick(() => {
                    vm.initialiseAssignedOfficerSelect(true);
                    vm.updateAssignedOfficerSelect();
                });
            }, (error) => {
                vm.feeWaiver = helpers.copyObject(vm.original_feeWaiver)
                vm.feeWaiver.applicant.address = vm.feeWaiver.applicant.address != null ? vm.feeWaiver.applicant.address : {};
                swal(
                    'Proposal Error',
                    helpers.apiVueResourceError(error),
                    'error'
                )
            });
            }
        },

        initialiseAssignedOfficerSelect:function(reinit=false){
            let vm = this;
            if (reinit){
                $(vm.$refs.assigned_officer).data('select2') ? $(vm.$refs.assigned_officer).select2('destroy'): '';
            }
            // Assigned officer select
            $(vm.$refs.assigned_officer).select2({
                "theme": "bootstrap",
                allowClear: true,
                placeholder:"Select Officer"
            }).
            on("select2:select",function (e) {
                var selected = $(e.currentTarget);
                /*
                if (vm.feeWaiver.processing_status == 'With Approver'){
                    vm.feeWaiver.assigned_approver = selected.val();
                }
                else{
                    vm.feeWaiver.assigned_officer = selected.val();
                }
                */
                vm.feeWaiver.assigned_officer = selected.val();
                vm.assignTo();
            }).on("select2:unselecting", function(e) {
                var self = $(this);
                setTimeout(() => {
                    self.select2('close');
                }, 0);
            }).on("select2:unselect",function (e) {
                var selected = $(e.currentTarget);
                /*
                if (vm.feeWaiver.processing_status == 'With Approver'){
                    vm.feeWaiver.assigned_approver = null;
                }
                else{
                    vm.feeWaiver.assigned_officer = null;
                }
                */
                vm.feeWaiver.assigned_officer = null;
                vm.assignTo();
            });
        },


    },
    mounted: function() {
        this.$nextTick(() => {
            Vue.http.get(`/api/feewaivers/${this.feeWaiverId}.json`).then(res => {
                  this.feeWaiver = res.body;
            },
            err => {
              console.log(err);
            });
        });
    },
    updated: function(){
        this.$nextTick(() => {
            this.initialiseAssignedOfficerSelect()
        });
        /*
        let vm = this;
        if (!vm.panelClickersInitialised){
            $('.panelClicker[data-toggle="collapse"]').on('click', function () {
                var chev = $(this).children()[0];
                window.setTimeout(function () {
                    $(chev).toggleClass("glyphicon-chevron-down glyphicon-chevron-up");
                },100);
            });
            vm.panelClickersInitialised = true;
        }
        this.$nextTick(() => {
            vm.initialiseOrgContactTable();
            vm.initialiseSelects();
            vm.form = document.forms.new_feeWaiver;
            if(vm.hasAmendmentRequest){
                vm.deficientFields();
            }
        });
        */
    },
    created: function() {
    },
    beforeRouteEnter: function(to, from, next) {
        next(vm => {
            vm.feeWaiverId = to.params.fee_waiver_id;
        })
    }
    /*
    beforeRouteEnter: function(to, from, next) {
          Vue.http.get(`/api/feeWaiver/${to.params.feeWaiver_id}/internal_feeWaiver.json`).then(res => {
              next(vm => {
                  vm.feeWaiver = res.body;
                  console.log(res.body)
                  vm.original_feeWaiver = helpers.copyObject(res.body);
                  if (vm.feeWaiver.applicant) {
                      vm.feeWaiver.applicant.address = vm.feeWaiver.applicant.address != null ? vm.feeWaiver.applicant.address : {};
                  }
                  vm.hasAmendmentRequest=vm.feeWaiver.hasAmendmentRequest;
              });
            },
            err => {
              console.log(err);
            });
    },
    beforeRouteUpdate: function(to, from, next) {
        console.log("beforeRouteUpdate");
          Vue.http.get(`/api/feeWaiver/${to.params.feeWaiver_id}.json`).then(res => {
              next(vm => {
                  vm.feeWaiver = res.body;
                  vm.original_feeWaiver = helpers.copyObject(res.body);
                  if (vm.feeWaiver.applicant) {
                      vm.feeWaiver.applicant.address = vm.feeWaiver.applicant.address != null ? vm.feeWaiver.applicant.address : {};
                  }
              });
            },
            err => {
              console.log(err);
            });
    }
    */
}
</script>
<style scoped>
.top-buffer-s {
    margin-top: 10px;
}
.actionBtn {
    cursor: pointer;
}
.hidePopover {
    display: none;
}
.separator {
    border: 1px solid;
    margin-top: 15px;
    margin-bottom: 10px;
    width: 100%;
}
</style>
