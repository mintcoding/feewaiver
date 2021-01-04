<template id="proposal_dashboard">
    <div class="container">
        <FormSection :formCollapse="false" label="Fee Waiver Requests" Index="fee_waiver_requests">
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
import ResponsiveDatatablesHelper from "@/utils/responsive_datatable_helper.js"
//require("bootstrap/dist/css/bootstrap.css");
import {
    api_endpoints,
    helpers
}from '@/utils/hooks'
export default {
    name: 'FeeWaiverDash',
    props: {
    },
    data() {
        let vm = this;
        return {
            url: '/api/feewaivers_paginated/feewaiver_internal/?format=datatables',
            pBody: 'pBody' + vm._uid,
            datatable_id: 'feewaiver-datatable-'+vm._uid,
            //Profile to check if user has access to process Proposal
            profile: {},
            show_spinner: false, 
            popoversInitialised: false,
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
            feewaiver_headers:["Lodgement Number", "Participant", "Status", "Lodged on", "Document", "Assigned To", "", "", "Action", "Comments to applicant"],
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
                    /*
                    {
                        data: "contact_name",
                        visible: true,
                        orderable: false,
                    },
                    */
                    {
                        data: "participants",
                        visible: true,
                        orderable: false,
                    },
                    {
                        data: "processing_status",
                        mRender:function (data,type,full) {
                            //return data != '' && data != null ? moment(data).format(vm.dateFormat): '';
                            let fullStatus = full.processing_status;
                            /*
                            if (full.processing_status === "With Approver" && full.proposed_status) {
                                fullStatus += '<br>(' + full.proposed_status + ')';
                            }
                            */
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
                        data: "latest_feewaiver_document",
                        visible: true,
                        orderable: false,
                        mRender:function(data,type,full){
                            //console.log(full)
                            if (data) {
                                return `<a href="${data}" target="_blank"><i style="color:red" class="fa fa-file-pdf-o"></i></a>`;
                            } else {
                                return null;
                            }
                        },

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
                    {
                        data: "can_process",
                        mRender:function (data,type,full) {
                            //let links = '';
                            let links = full.action_shortcut;
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
                    {
                        data: "comments_to_applicant",
                        visible: true,
                        mRender: function (value) {
                            var ellipsis = '...',
                                truncated = _.truncate(value, {
                                    length: 25,
                                    omission: ellipsis,
                                    separator: ' '
                                }),
                                result = '<span>' + truncated + '</span>',
                                popTemplate = _.template('<a href="#" ' +
                                    'role="button" ' +
                                    'data-toggle="popover" ' +
                                    'data-trigger="click" ' +
                                    'data-placement="top auto"' +
                                    'data-html="true" ' +
                                    'data-content="<%= text %>" ' +
                                    '>more</a>');
                            if (_.endsWith(truncated, ellipsis)) {
                                result += popTemplate({
                                    text: value
                                });
                            }

                            return result;
                        },

                        'createdCell': function (cell) {
                            //TODO why this is not working?
                            // the call to popover is done in the 'draw' event
                            $(cell).popover();
                        }
                        //responsivePriority: 50,
                        //width: "50%",
                        //searchable: false,
                    },
                    {
                        data: "id",
                        visible: false,
                        orderable: false,
                    },


                ],
                processing: true,
                initComplete: function() {
                    //vm.$refs.feewaiver_datatable.vmDataTable.columns.adjust().responsive.recalc().draw();
                    //console.log(vm.$refs.feewaiver_datatable.vmDataTable.columns)
                    vm.$refs.feewaiver_datatable.vmDataTable.columns.adjust().draw();
                },
            }
        }
    },
    components:{
        FormSection,
        datatable,
    },
    watch:{
        filterFeeWaiverStatus: function(){
            this.$refs.feewaiver_datatable.vmDataTable.draw();
        },

        filterFeeWaiverLodgedFrom: function(){
            this.$refs.feewaiver_datatable.vmDataTable.draw();
        },
        filterFeeWaiverLodgedTo: function(){
            this.$refs.feewaiver_datatable.vmDataTable.draw();
        }
    },
    computed: {
    },
    methods:{
        fetchFilterLists: function(){
            let vm = this;

            vm.$http.get(api_endpoints.filter_list).then((response) => {
                vm.feewaiver_status = response.body.feewaiver_status_choices;
            },(error) => {
                console.log(error);
            })
            //console.log(vm.regions);
        },
        actionShortcut: async function(id, approvalType) {
            let vm = this;
            let processingTableStr = `.action-${id}`;
            let processingTable = $(processingTableStr);
            processingTable.replaceWith("<div><i class='fa fa-2x fa-spinner fa-spin'></i></div>");
            //processingTable.replaceWith = "<i class='fa fa-2x fa-spinner fa-spin'></i>"
            //let table = vm.$refs.feewaiver_datatable.vmDataTable
            //table.data("processing.dt", true);
            let post_url = '/api/feewaivers/' + id + '/final_approval/'
            let res = await Vue.http.post(post_url, {'approval_type': approvalType});
            if (res.ok) {
                this.refreshFromResponse();
            }
            //table.data("processing.dt", false);
        },
        refreshFromResponse: function(){
            this.$refs.feewaiver_datatable.vmDataTable.ajax.reload();
        },
        initialisePopovers: function(){
            if (!this.popoversInitialised){
                //this.initialiseActionLogs(this._uid,this.$refs.showActionBtn,this.actionsDtOptions,this.actionsTable);
                //this.initialiseCommLogs('-internal-proposal-'+this._uid,this.$refs.showCommsBtn,this.commsDtOptions,this.commsTable);
                this.popoversInitialised = true;
            }
        },
        initialiseDash: function(vm_uid,ref,datatable_options,table){
            let vm = this;
            let commsLogId = 'comms-log-table'+vm_uid;
            let popover_name = 'popover-'+ vm._uid+'-comms';
            $(ref).popover({
                content: function() {
                    return ` 
                    <table id="${commsLogId}" class="hover table table-striped table-bordered dt-responsive " cellspacing="0" width="100%">
                    </table>`
                },
                html: true,
                title: 'Communications Log',
                container: 'body',
                placement: 'right',
                trigger: "click",
                template: `<div class="popover ${popover_name}" role="tooltip"><div class="arrow"></div><h3 class="popover-title"></h3><div class="popover-content"></div></div>`,
            }).on('inserted.bs.popover', function () {
                table = $('#'+commsLogId).DataTable(datatable_options);

                // activate popover when table is drawn.
                table.on('draw.dt', function () {
                    var $tablePopover = $(this).find('[data-toggle="popover"]');
                    if ($tablePopover.length > 0) {
                        $tablePopover.popover();
                        // the next line prevents from scrolling up to the top after clicking on the popover.
                        $($tablePopover).on('click', function (e) {
                            e.preventDefault();
                            return true;   
                        });
                    }
                });
            }).on('shown.bs.popover', function () {
                var el = ref;
                var popoverheight = parseInt($('.'+popover_name).height());

                var popover_bounding_top = parseInt($('.'+popover_name)[0].getBoundingClientRect().top);
                var popover_bounding_bottom = parseInt($('.'+popover_name)[0].getBoundingClientRect().bottom);

                var el_bounding_top = parseInt($(el)[0].getBoundingClientRect().top);
                var el_bounding_bottom = parseInt($(el)[0].getBoundingClientRect().top);
                
                var diff = el_bounding_top - popover_bounding_top;

                var position = parseInt($('.'+popover_name).position().top);
                var pos2 = parseInt($(el).position().top) - 5;

                var x = diff + 5;
                $('.'+popover_name).children('.arrow').css('top', x + 'px');
            });

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
            let table = vm.$refs.feewaiver_datatable.vmDataTable
            table.on('processing.dt', function(e) {
                console.log("processing");
            })
            table.on('click', 'a[data-issue]', async function(e) {
                //let processingTable = $(vm.$refs.feewaiver_datatable.table).filter('[data-issue]')
                e.preventDefault();
                //vm.$refs.feewaiver_datatable.vmDataTable.draw();
                var id = $(this).attr('data-issue');
                /*
                let processingTable = $(vm.$refs.feewaiver_datatable.table)
                //processingTable.replaceWith = "<div><i class='fa fa-2x fa-spinner fa-spin'></i></div>"
                processingTable.replaceWith('<div class="spinner-border" role="status"><span class="sr-only">Loading...</span></div>')
                console.log(processingTable);
                */
                await vm.actionShortcut(id, 'issue');
            }).on('click', 'a[data-concession]', async function(e) {
                e.preventDefault();
                var id = $(this).attr('data-concession');
                await vm.actionShortcut(id, 'issue_concession');
            }).on('click', 'a[data-decline]', async function(e) {
                e.preventDefault();
                var id = $(this).attr('data-decline');
                await vm.actionShortcut(id, 'decline');
            //}).on('inserted.bs.popover', function () {
                //table = $('#'+commsLogId).DataTable(datatable_options);

                // activate popover when table is drawn.
            }).on('draw.dt', function () {
                var tablePopover = $(this).find('[data-toggle="popover"]');
                //console.log(tablePopover)
                if (tablePopover.length > 0) {
                    tablePopover.popover();
                    // the next line prevents from scrolling up to the top after clicking on the popover.
                    $(tablePopover).on('click', function (e) {
                        e.preventDefault();
                        return true;   
                    });
                }
            });

        },
        initialiseSearch:function(){
            //this.regionSearch();
            this.dateSearch();
        },
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
        /*
        this.$nextTick(() => {
            vm.initialisePopovers();
        });
        */
    },
    updated: function() {
        this.$nextTick(() => {
            this.initialiseSearch();
            this.addEventListeners();
            //this.setDashboardText();
        });
    },
    created: function() {
    },

}
</script>
<style scoped>
</style>
