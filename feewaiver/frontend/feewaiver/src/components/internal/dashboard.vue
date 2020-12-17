<template id="proposal_dashboard">
    <div class="container">
        <FormSection>
                    <div class="row">
                        <div class="col-md-3">
                            <label for="">Lodged From</label>
                            <div class="input-group date" ref="feewaiverDateFromPicker">
                                <input type="text" class="form-control" placeholder="DD/MM/YYYY" v-model="filterFeeWaiverLodgedFrom">
                                <span class="input-group-addon">
                                    <span class="glyphicon glyphicon-calendar"></span>
                                </span>
                            </div>
                        </div>
                        <div class="col-md-3">
                            <label for="">Lodged To</label>
                            <div class="input-group date" ref="feewaiverDateToPicker">
                                <input type="text" class="form-control" placeholder="DD/MM/YYYY" v-model="filterFeeWaiverLodgedTo">
                                <span class="input-group-addon">
                                    <span class="glyphicon glyphicon-calendar"></span>
                                </span>
                            </div>
                        </div>
                        <div class="col-md-3">
                            <div class="form-group">
                                <label for="">Status</label>
                                <select class="form-control" v-model="filterFeeWaiverStatus">
                                    <option value="All">All</option>
                                    <option v-for="s in feewaiver_status" :value="s">{{s}}</option>
                                </select>
                            </div>
                        </div>
                    </div>
                    <!--div class="row">
                        <div class="col-md-3">
                            <label for="">Expiry From</label>
                            <div class="input-group date" ref="proposalDateFromPicker">
                                <input type="text" class="form-control" placeholder="DD/MM/YYYY" v-model="filterProposalLodgedFrom">
                                <span class="input-group-addon">
                                    <span class="glyphicon glyphicon-calendar"></span>
                                </span>
                            </div>
                        </div>
                        <div class="col-md-3">
                            <label for="">Expiry To</label>
                            <div class="input-group date" ref="proposalDateToPicker">
                                <input type="text" class="form-control" placeholder="DD/MM/YYYY" v-model="filterProposalLodgedTo">
                                <span class="input-group-addon">
                                    <span class="glyphicon glyphicon-calendar"></span>
                                </span>
                            </div>
                        </div>
                    </div-->
                    <div class="row">
                        <div class="col-lg-12" style="margin-top:25px;">
                            <datatable ref="feewaiver_datatable" :id="datatable_id" :dtOptions="feewaiver_options" :dtHeaders="feewaiver_headers"/>
                        </div>
                    </div>
        </FormSection>
        </div>
</template>
<script>

import datatable from '@/utils/vue/datatable.vue'
import Vue from 'vue'
import FormSection from "@/components/forms/section_toggle.vue"
/*
import ApprovalCancellation from '../internal/approvals/approval_cancellation.vue'
import ApprovalSuspension from '../internal/approvals/approval_suspension.vue'
import ApprovalSurrender from '../internal/approvals/approval_surrender.vue'
import ApprovalHistory from './approval_history_modal.vue';
*/
import {
    api_endpoints,
    helpers
}from '@/utils/hooks'
export default {
    name: 'FeeWaiverDash',
    props: {
        /*
        level:{
            type: String,
            required: true,
            validator:function(val) {
                let options = ['internal','referral','external'];
                return options.indexOf(val) != -1 ? true: false;
            }
        },
        url:{
            type: String,
            required: true
        }
        */
    },
    data() {
        let vm = this;
        return {
            url: '/api/feewaivers_paginated/feewaiver_internal/?format=datatables',
            pBody: 'pBody' + vm._uid,
            datatable_id: 'feewaiver-datatable-'+vm._uid,
            //Profile to check if user has access to process Proposal
            profile: {},
            /*
            approval_history: {
                isModalOpen: false,
                approval_history_id: null,
            },
            */
            // Filters for Proposals
            //filterProposalRegion: 'All',
            //filterProposalActivity: 'All',
            filterFeeWaiverStatus: 'All',
            filterFeeWaiverLodgedFrom: '',
            filterFeeWaiverLodgedTo: '',
            //filterProposalSubmitter: 'All',
            dashboardTitle: '',
            dashboardDescription: '',
            dateFormat: 'DD/MM/YYYY',
            datepickerOptions:{
                format: 'DD/MM/YYYY',
                showClear:true,
                useCurrent:false,
                keepInvalid:true,
                allowInputToggle:true
            },
            feewaiver_status:[],
            /*
            proposal_activityTitles : [],
            proposal_regions: [],
            proposal_submitters: [],
            //template_group: '',
            dasTemplateGroup: false,
            apiaryTemplateGroup: false,
            */
            //feewaiver_headers:["Number","Submitter","Status","Lodged On","Document","Assigned To","Action"],
            feewaiver_headers:["Lodgement Number", "Submitter", "Status", "Lodged on", "Document", "Assigned To", "", "", "Action"],
            feewaiver_options:{
                language: {
                    processing: "<i class='fa fa-4x fa-spinner fa-spin'></i>"
                },
                responsive: true,
                serverSide: true,
                //lengthMenu: [ [10, 25, 50, 100, -1], [10, 25, 50, 100, "All"] ],
                order: [
                    [0, 'desc']
                    ],
                ajax: {
                    //"url": vm.url,
                    "url": '/api/feewaivers_paginated/feewaiver_internal/?format=datatables',
                    "dataSrc": 'data',
                    // adding extra GET params for Custom filtering
                    "data": function ( d ) {
                        d.date_from = vm.filterFeeWaiverLodgedFrom != '' && vm.filterFeeWaiverLodgedFrom != null ? moment(vm.filterFeeWaiverLodgedFrom, 'DD/MM/YYYY').format('YYYY-MM-DD'): '';
                        d.date_to = vm.filterFeeWaiverLodgedTo != '' && vm.filterFeeWaiverLodgedTo != null ? moment(vm.filterFeeWaiverLodgedTo, 'DD/MM/YYYY').format('YYYY-MM-DD'): '';
                        d.processing_status = vm.filterFeeWaiverStatus;
                    }

                },
                dom: 'lBfrtip',
                buttons:[
                    {
                        extend: 'excel',
                        exportOptions: {
                            columns: ':visible'
                        }
                    },
                    {
                        extend: 'csv',
                        exportOptions: {
                            columns: ':visible'
                        }
                    },
                ],
                columns: [
                    {
                        data: "lodgement_number",
                        visible: true,
                        //searchable: false,
                    },
                    {
                        data: "contact_name",
                        visible: true,
                        orderable: false,
                    },
                    {
                        data: "processing_status",
                        mRender:function (data,type,full) {
                            //return data != '' && data != null ? moment(data).format(vm.dateFormat): '';
                            let fullStatus = full.processing_status;
                            if (full.processing_status === "With Approver" && full.proposed_status) {
                                fullStatus += '<br>(' + full.proposed_status + ')';
                            }
                            return fullStatus
                        },
                        //searchable: false,
                        visible: true,
                    },
                    {
                        data: "lodgement_date",
                        mRender:function (data,type,full) {
                            return data != '' && data != null ? moment(data).format(vm.dateFormat): '';
                        },
                        visible: true,
                    },
                    {
                        data: "id",
                        visible: true,
                        orderable: false,
                        //searchable: false,
                    },
                    {
                        data: "assigned_officer",
                        visible: true,
                        //searchable: false,
                    },
                    {
                        data: "proposed_status",
                        visible: false,
                        //searchable: false,
                    },
                    {
                        data: "action_shortcut",
                        visible: false,
                        //searchable: false,
                    },
                    /*
                    {
                        data: "user_action",
                        searchable: false,
                        orderable: false
                    },
                    {
                        data: "id",
                        visible: true,
                        orderable: false,
                        //searchable: false,
                    },
                    */
                    {
                        data: "can_process",
                        mRender:function (data,type,full) {
                            //let links = '';
                            let links = full.action_shortcut;
                            //console.log(full)
                            if(full.can_process){

                                links +=  `<a href='/internal/fee_waiver/${full.id}'>Process</a><br/>`;
                            } else{
                                links +=  `<a href='/internal/fee_waiver/${full.id}'>View</a><br/>`;
                            }
                            return links;
                        },
                        name: '',
                        searchable: false,
                        orderable: false
                    },



                ],
                processing: true,
                /*
                initComplete: function() {
                },
                */
            }
        }
    },
    components:{
        FormSection,
        datatable,
    },
    watch:{
        /*
        filterFeeWaiverStatus: function(){
            //this.$refs.proposal_datatable.vmDataTable.draw();
            let vm = this;
            if (vm.filterFeeWaiverStatus!= 'All') {
                vm.$refs.feewaiver_datatable.vmDataTable.columns(2).search(vm.filterFeeWaiverStatus).draw();
            } else {
                vm.$refs.feewaiver_datatable.vmDataTable.columns(2).search('').draw();
            }
        },
        */
        filterFeeWaiverStatus: function(){
            this.$refs.feewaiver_datatable.vmDataTable.draw();
        },

        filterFeeWaiverLodgedFrom: function(){
            this.$refs.feewaiver_datatable.vmDataTable.draw();
        },
        filterFeeWaiverLodgedTo: function(){
            this.$refs.feewaiver_datatable.vmDataTable.draw();
        }
        /*
        filterProposalRegion: function(){
            //this.$refs.proposal_datatable.vmDataTable.draw();
            let vm = this;
            if (vm.filterProposalRegion!= 'All') {
                vm.$refs.proposal_datatable.vmDataTable.columns(1).search(vm.filterProposalRegion).draw();
            } else {
                vm.$refs.proposal_datatable.vmDataTable.columns(1).search('').draw();
            }
        },
        filterProposalActivity: function() {
            let vm = this;
            if (vm.filterProposalActivity!= 'All') {
                vm.$refs.proposal_datatable.vmDataTable.columns(2).search(vm.filterProposalActivity).draw();
            } else {
                vm.$refs.proposal_datatable.vmDataTable.columns(2).search('').draw();
            }
        },
        filterProposalSubmitter: function(){
            //this.$refs.proposal_datatable.vmDataTable.draw();
            let vm = this;
            if (vm.filterProposalSubmitter!= 'All') {
                vm.$refs.proposal_datatable.vmDataTable.columns(4).search(vm.filterProposalSubmitter).draw();
            } else {
                vm.$refs.proposal_datatable.vmDataTable.columns(4).search('').draw();
            }

        },
        filterProposalStatus: function() {
            let vm = this;
            if (vm.filterProposalStatus!= 'All') {
                vm.$refs.proposal_datatable.vmDataTable.columns(5).search(vm.filterProposalStatus).draw();
            } else {
                vm.$refs.proposal_datatable.vmDataTable.columns(5).search('').draw();
            }
        },
        filterProposalLodgedFrom: function(){
            this.$refs.proposal_datatable.vmDataTable.draw();
        },
        filterProposalLodgedTo: function(){
            this.$refs.proposal_datatable.vmDataTable.draw();
        }
        */
    },
    computed: {
        /*
        status: function(){
            //return this.is_external ? this.external_status : this.internal_status;
            return [];
        },
        is_external: function(){
            return this.level == 'external';
        },
        is_referral: function(){
            return this.level == 'referral';
        },
        */
    },
    methods:{
        /*
        setDashboardText: function() {
            //let title = ''
            if (this.apiaryTemplateGroup) {
                this.dashboardTitle = 'Licences';
                this.dashboardDescription = 'View existing licences and amend or renew them';
            } else {
                this.dashboardTitle = 'Approvals';
                this.dashboardDescription = 'View existing approvals and amend or renew them';
            }
            //return title;
        },

        */
        fetchFilterLists: function(){
            let vm = this;

            vm.$http.get(api_endpoints.filter_list).then((response) => {
                /*
                vm.proposal_regions = response.body.regions;
                vm.proposal_activityTitles = response.body.activities;
                vm.proposal_submitters = response.body.submitters;
                */
                vm.feewaiver_status = response.body.feewaiver_status_choices;
            },(error) => {
                console.log(error);
            })
            //console.log(vm.regions);
        },
        actionShortcut: async function(id, workflowAction) {
            let post_url = '/api/feewaivers/' + id + '/workflow_action/'
            let res = await Vue.http.post(post_url, {'workflow_type': workflowAction});
            if (res.ok) {
                this.refreshFromResponse();
            }
        },
        refreshFromResponse: function(){
            this.$refs.feewaiver_datatable.vmDataTable.ajax.reload();
        },

        addEventListeners: function(){
            let vm = this;
            // Initialise Proposal Date Filters
            $(vm.$refs.feewaiverDateToPicker).datetimepicker(vm.datepickerOptions);
            $(vm.$refs.feewaiverDateToPicker).on('dp.change', function(e){
                if ($(vm.$refs.feewaiverDateToPicker).data('DateTimePicker').date()) {
                    vm.filterFeeWaiverLodgedTo =  e.date.format('DD/MM/YYYY');
                }
                else if ($(vm.$refs.feewaiverDateToPicker).data('date') === "") {
                    vm.filterFeeWaiverLodgedTo = "";
                }
             });
            $(vm.$refs.feewaiverDateFromPicker).datetimepicker(vm.datepickerOptions);
            $(vm.$refs.feewaiverDateFromPicker).on('dp.change',function (e) {
                if ($(vm.$refs.feewaiverDateFromPicker).data('DateTimePicker').date()) {
                    vm.filterFeeWaiverLodgedFrom = e.date.format('DD/MM/YYYY');
                    $(vm.$refs.feewaiverDateToPicker).data("DateTimePicker").minDate(e.date);
                }
                else if ($(vm.$refs.feewaiverDateFromPicker).data('date') === "") {
                    vm.filterFeeWaiverLodgedFrom = "";
                }
            });
            //Internal Action shortcut listeners
            vm.$refs.feewaiver_datatable.vmDataTable.on('click', 'a[data-issue]', function(e) {
                e.preventDefault();
                var id = $(this).attr('data-issue');
                vm.actionShortcut(id, 'issue');
                //var id = $(this).attr('data-cancel-approval');
                //vm.cancelApproval(id);
            });
            vm.$refs.feewaiver_datatable.vmDataTable.on('click', 'a[data-concession]', function(e) {
                e.preventDefault();
                var id = $(this).attr('data-concession');
                vm.actionShortcut(id, 'issue_concession');
            });
            vm.$refs.feewaiver_datatable.vmDataTable.on('click', 'a[data-decline]', function(e) {
                e.preventDefault();
                var id = $(this).attr('data-decline');
                vm.actionShortcut(id, 'decline');
            });

            /*
            // End Proposal Date Filters
            // Internal Reissue listener
            vm.$refs.proposal_datatable.vmDataTable.on('click', 'a[data-reissue-approval]', function(e) {
                e.preventDefault();
                var id = $(this).attr('data-reissue-approval');
                vm.reissueApproval(id);
            });

            //Internal Cancel listener
            vm.$refs.proposal_datatable.vmDataTable.on('click', 'a[data-cancel-approval]', function(e) {
                e.preventDefault();
                var id = $(this).attr('data-cancel-approval');
                vm.cancelApproval(id);
            });

            //Internal Suspend listener
            vm.$refs.proposal_datatable.vmDataTable.on('click', 'a[data-suspend-approval]', function(e) {
                e.preventDefault();
                var id = $(this).attr('data-suspend-approval');
                vm.suspendApproval(id);
            });

            // Internal Reinstate listener
            vm.$refs.proposal_datatable.vmDataTable.on('click', 'a[data-reinstate-approval]', function(e) {
                e.preventDefault();
                var id = $(this).attr('data-reinstate-approval');
                vm.reinstateApproval(id);
            });

            //Internal/ External Surrender listener
            vm.$refs.proposal_datatable.vmDataTable.on('click', 'a[data-surrender-approval]', function(e) {
                e.preventDefault();
                var id = $(this).attr('data-surrender-approval');
                vm.surrenderApproval(id);
            });

            // External renewal listener
            vm.$refs.proposal_datatable.vmDataTable.on('click', 'a[data-renew-approval]', function(e) {
                e.preventDefault();
                var id = $(this).attr('data-renew-approval');
                vm.renewApproval(id);
            });

            // External amend listener
            vm.$refs.proposal_datatable.vmDataTable.on('click', 'a[data-amend-approval]', function(e) {
                e.preventDefault();
                var id = $(this).attr('data-amend-approval');
                vm.amendApproval(id);
            });

            // Internal view pdf listener
            vm.$refs.proposal_datatable.vmDataTable.on('click', 'a[data-pdf-approval]', function(e) {
                e.preventDefault();
                var id = $(this).attr('data-pdf-approval');
                var media_link = $(this).attr('media-link');
                vm.viewApprovalPDF(id, media_link);
            });
            // Create Licence History Listener.
            vm.$refs.proposal_datatable.vmDataTable.on('click', 'a[approval-history]', function(e) {
                e.preventDefault();
                let approval_id = $(this).attr('approval-history');
                vm.$refs.approval_history.approval_history_id = approval_id;
                vm.$refs.approval_history.isModalOpen = true;
            });
            */
        },
        initialiseSearch:function(){
            //this.regionSearch();
            this.dateSearch();
        },
        /*
        regionSearch:function(){
            let vm = this;
            vm.$refs.proposal_datatable.table.dataTableExt.afnFiltering.push(
                function(settings,data,dataIndex,original){
                    let found = false;
                    let filtered_regions = vm.filterProposalRegion.split(',');
                    if (filtered_regions == 'All'){ return true; }

                    let regions = original.region != '' && original.region != null ? original.region.split(','): [];

                    $.each(regions,(i,r) => {
                        if (filtered_regions.indexOf(r) != -1){
                            found = true;
                            return false;
                        }
                    });
                    if  (found) { return true; }

                    return false;
                }
            );
        },
        submitterSearch:function(){
            let vm = this;
            vm.$refs.proposal_datatable.table.dataTableExt.afnFiltering.push(
                function(settings,data,dataIndex,original){
                    let filtered_submitter = vm.filterProposalSubmitter;
                    if (filtered_submitter == 'All'){ return true; }
                    return filtered_submitter == original.submitter.email;
                }
            );
        },
        */
        dateSearch:function(){
            let vm = this;
            vm.$refs.feewaiver_datatable.table.dataTableExt.afnFiltering.push(
                function(settings,data,dataIndex,original){
                    let from = vm.filterFeeWaiverLodgedFrom;
                    let to = vm.filterFeeWaiverLodgedTo;
                    let val = original.lodgement_date;

                    if ( from == '' && to == ''){
                        return true;
                    }
                    else if (from != '' && to != ''){
                        return val != null && val != '' ? moment().range(moment(from,vm.dateFormat),moment(to,vm.dateFormat)).contains(moment(val)) :false;
                    }
                    else if(from == '' && to != ''){
                        if (val != null && val != ''){
                            return moment(to,vm.dateFormat).diff(moment(val)) >= 0 ? true : false;
                        }
                        else{
                            return false;
                        }
                    }
                    else if (to == '' && from != ''){
                        if (val != null && val != ''){
                            return moment(val).diff(moment(from,vm.dateFormat)) >= 0 ? true : false;
                        }
                        else{
                            return false;
                        }
                    }
                    else{
                        return false;
                    }
                }
            );
        },
        /*
        fetchProfile: function(){
            let vm = this;
            Vue.http.get(api_endpoints.profile).then((response) => {
                vm.profile = response.body

            },(error) => {
                console.log(error);

            })
        },

        check_assessor: function(proposal){
            let vm = this;
            //console.log(proposal.id, proposal.can_approver_reissue);
            var assessor = proposal.allowed_assessors.filter(function(elem){
                    return(elem.id==vm.profile.id)

                });

            if (assessor.length > 0){
                //console.log(proposal.id, assessor)
                return true;
            }
            else
                return false;

            return false;
        },

        reissueApproval:function (proposal_id) {
            let vm = this;
            let status= 'with_approver'
            let data = {'status': status}
            swal({
                title: "Reissue Approval",
                text: "Are you sure you want to reissue this approval?",
                type: "warning",
                showCancelButton: true,
                confirmButtonText: 'Reissue approval',
                //confirmButtonColor:'#d9534f'
            }).then(() => {
                vm.$http.post(helpers.add_endpoint_json(api_endpoints.proposals,(proposal_id+'/reissue_approval')),JSON.stringify(data),{
                emulateJSON:true,
                })
                .then((response) => {

                    vm.$router.push({
                    name:"internal-proposal",
                    params:{proposal_id:proposal_id}
                    });
                }, (error) => {
                    console.log(error);
                    swal({
                    title: "Reissue Approval",
                    text: error.body,
                    type: "error",
                    })
                });
            },(error) => {

            });
        },

        reinstateApproval:function (approval_id) {
            let vm = this;
            let status= 'with_approver'
            //let data = {'status': status}
            swal({
                title: "Reinstate Approval",
                text: "Are you sure you want to reinstate this approval?",
                type: "warning",
                showCancelButton: true,
                confirmButtonText: 'Reinstate approval',
                //confirmButtonColor:'#d9534f'
            }).then(() => {
                vm.$http.post(helpers.add_endpoint_json(api_endpoints.approvals,(approval_id+'/approval_reinstate')),{

                })
                .then((response) => {
                    swal(
                        'Reinstate',
                        'Your approval has been reinstated',
                        'success'
                    )
                    vm.$refs.proposal_datatable.vmDataTable.ajax.reload();

                }, (error) => {
                    console.log(error);
                    swal({
                    title: "Reinstate Approval",
                    text: error.body,
                    type: "error",
                    })
                });
            },(error) => {

            });
        },

        renewApproval:function (proposal_id) {
            let vm = this;
            let status= 'with_approver'
            //let data = {'status': status}
            swal({
                title: "Renew Approval",
                text: "Are you sure you want to renew this approval?",
                type: "warning",
                showCancelButton: true,
                confirmButtonText: 'Renew approval',
                //confirmButtonColor:'#d9534f'
            }).then(() => {
                vm.$http.get(helpers.add_endpoint_json(api_endpoints.proposals,(proposal_id+'/renew_approval')),{

                })
                .then((response) => {
                   let proposal = {}
                   proposal = response.body
                   vm.$router.push({
                    name:"draft_proposal",
                    params:{proposal_id: proposal.id}
                   });

                }, (error) => {
                    console.log(error);
                    swal({
                    title: "Renew Approval",
                    text: error.body,
                    type: "error",
                    })
                });
            },(error) => {

            });
        },

        amendApproval:function (proposal_id) {
            let vm = this;
            swal({
                title: "Amend Approval",
                text: "Are you sure you want to amend this approval?",
                type: "warning",
                showCancelButton: true,
                confirmButtonText: 'Amend approval',
                //confirmButtonColor:'#d9534f'
            }).then(() => {
                vm.$http.get(helpers.add_endpoint_json(api_endpoints.proposals,(proposal_id+'/amend_approval')),{

                })
                .then((response) => {
                   let proposal = {}
                   proposal = response.body
                   vm.$router.push({
                    name:"draft_proposal",
                    params:{proposal_id: proposal.id}
                   });

                }, (error) => {
                    console.log(error);
                    swal({
                    title: "Amend Approval",
                    text: error.body,
                    type: "error",
                    })

                });
            },(error) => {

            });
        },

        cancelApproval: function(approval_id){

            this.$refs.approval_cancellation.approval_id = approval_id;
            this.$refs.approval_cancellation.isModalOpen = true;
        },

        suspendApproval: function(approval_id){
            this.$refs.approval_suspension.approval = {};
            this.$refs.approval_suspension.approval_id = approval_id;
            this.$refs.approval_suspension.isModalOpen = true;
        },

        surrenderApproval: function(approval_id){

            this.$refs.approval_surrender.approval_id = approval_id;
            this.$refs.approval_surrender.isModalOpen = true;
        },

        refreshFromResponse: function(){
            this.$refs.proposal_datatable.vmDataTable.ajax.reload();
        },

        viewApprovalPDF: function(id,media_link){
            let vm=this;
            //console.log(approval);
            vm.$http.get(helpers.add_endpoint_json(api_endpoints.approvals,(id+'/approval_pdf_view_log')),{
                })
                .then((response) => {
                    //console.log(response)
                }, (error) => {
                    console.log(error);
                });
            window.open(media_link, '_blank');
        },
        */

    },
    mounted: function(){
		this.fetchFilterLists();
        //this.fetchProfile();
        let vm = this;
        $( 'a[data-toggle="collapse"]' ).on( 'click', function () {
            var chev = $( this ).children()[ 0 ];
            window.setTimeout( function () {
                $( chev ).toggleClass( "glyphicon-chevron-down glyphicon-chevron-up" );
            }, 100 );
        });
    },
    updated: function() {
        this.$nextTick(() => {
            this.initialiseSearch();
            this.addEventListeners();
            //this.setDashboardText();
        });
    },
    created: function() {
        /*
        // retrieve template group
        this.$http.get('/template_group',{
            emulateJSON:true
            }).then(res=>{
                //this.template_group = res.body.template_group;
                if (res.body.template_group === 'apiary') {
                    this.apiaryTemplateGroup = true;
                } else {
                    this.dasTemplateGroup = true;
                }
        },err=>{
        console.log(err);
        });
        */
    },

}
</script>
<style scoped>
</style>
