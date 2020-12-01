<template lang="html">
    <div class="container">
        <!--strong> fill in form</strong-->
        <!--a class="navbar-brand" href="{% url 'ds_home' %}"><div style="inline"><img src="{% static 'feewaiver/img/dpaw_small.png' %}">Staff login</div></a-->
        <!--a class="navbar-brand pull-right" href="/"><div style="inline"><img src="/static/feewaiver/img/dpaw_small.png">Staff login</div></a-->
        <FormSection :formCollapse="false" label="Contact Details" Index="contact_details">
            <div class="col-md-12">
                <div class="form-group">
                    <div class="row">
                    <label for="" class="col-sm-2 control-label">Organisation</label>
                    <div class="col-sm-4">
                        <input type="text" class="form-control" name="organisation" placeholder="" v-model="contactDetails.organisation">
                    </div>
                    <label for="" class="col-sm-2 control-label">Contact</label>
                    <div class="col-sm-4">
                        <input type="text" class="form-control" name="contact_name" placeholder="" v-model="contactDetails.contact_name">
                    </div>
                    </div>
                </div>
                <div class="form-group">
                    <div class="row">
                    <label for="" class="col-sm-2 control-label">Postal Address</label>
                    <div class="col-sm-4">
                        <input type="text" class="form-control" name="postal_address" placeholder="" v-model="contactDetails.postal_address">
                    </div>
                    </div>
                </div>
                <div class="form-group">
                    <div class="row">
                    <label for="suburb" class="col-sm-2 control-label">Suburb</label>
                    <div class="col-sm-4">
                        <input type="text" class="form-control" name="suburb" placeholder="" v-model="contactDetails.suburb">
                    </div>
                    <label for="state" class="col-sm-1 control-label">State</label>
                    <div class="col-sm-2">
                        <input type="text" class="form-control" name="state" placeholder="" v-model="contactDetails.state">
                    </div>
                    <label for="postcode" class="col-sm-1 control-label">Postcode</label>
                    <div class="col-sm-2">
                        <input type="text" class="form-control" name="postcode" placeholder="" v-model="contactDetails.postcode">
                    </div>
                    </div>
                </div>
                <div class="form-group">
                    <div class="row">
                    <label for="phone" class="col-sm-2 control-label">Phone</label>
                    <div class="col-sm-4">
                    <input type="text" class="form-control" name="phone" placeholder="" v-model="contactDetails.phone">
                    </div>
                    </div>
                </div>
                <div class="form-group">
                    <div class="row">
                    <label for="email" class="col-sm-2 control-label">Email</label>
                    <div class="col-sm-4">
                        <input type="text" class="form-control" name="email" placeholder="" v-model="contactDetails.email">
                    </div>
                    <label for="email_confirmation" class="col-sm-2 control-label">Confirm Email</label>
                    <div class="col-sm-4">
                    <input type="text" class="form-control" name="email_confirmation" placeholder="" v-model="email_confirmation">
                    </div>
                    </div>
                </div>
                <div class="form-group">
                    <div class="row">
                        <label class="col-sm-4 control-label">Participants</label>
                        <div class="col-sm-6">
                            <select ref="participants" class="form-control" v-model="contactDetails.participants_id">
                                <option value="null"></option>
                                <option v-for="group in participantGroupList" :value="group.id">{{group.name}}</option>
                            </select>
                        </div>
                    </div>
                </div>
                <div class="form-group">
                    <div class="row">
                      <label class="col-sm-4 control-label">Provide a brief explanation of your organisation</label>
                      <div class="col-sm-8">
                          <textarea class="form-control" v-model="contactDetails.organisation_details"/>
                      </div>
                    </div>
                </div>
            </div>
        </FormSection>
        <FormSection :formCollapse="false" label="Fee Waiver Request" Index="fee_waiver_request">
            <div class="col-sm-10">
                <div class="form-group">
                    <div class="row">
                      <label for="fee_waiver_purpose" class="col-sm-4 control-label">Describe the purpose of the visit(s)</label>
                      <div class="col-sm-8">
                          <textarea class="form-control" name="fee_waiver_purpose" v-model="feeWaiver.fee_waiver_purpose"/>
                      </div>
                    </div>
                </div>
            </div>
            <div class="col-sm-10">
                <div class="form-group">
                    <div class="row">
                        <label for="fee_waiver_description" class="col-sm-4 control-label">Provide the details of your visit</label>
                        <div class="col-sm-8">
                            <textarea class="form-control" name="fee_waiver_description" v-model="feeWaiver.fee_waiver_description"/>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-sm-10">
                <div class="form-group">
                    <div class="row">
                        <label for="date_from" class="col-sm-4 control-label">Date from</label>
                        <div class="col-sm-4">
                            <div class="input-group date" ref="dateFromPicker">
                                    <input name="date_from" type="text" class="form-control" placeholder="DD/MM/YYYY" v-model="feeWaiver.date_from" />
                                    <span class="input-group-addon">
                                        <span class="glyphicon glyphicon-calendar"></span>
                                    </span>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="form-group">
                    <div class="row">
                        <label for="date_to" class="col-sm-4 control-label">Date to</label>
                        <div class="col-sm-4">
                            <div class="input-group date" ref="dateToPicker">
                                    <input name="date_to" type="text" class="form-control" placeholder="DD/MM/YYYY" v-model="feeWaiver.date_to" />
                                    <span class="input-group-addon">
                                        <span class="glyphicon glyphicon-calendar"></span>
                                    </span>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="form-group">
                    <div class="row">
                        <label for="number_of_vehicles" class="col-sm-4 control-label">Number of vehicles used for visit</label>
                        <div class="col-sm-4">
                            <input type="number" class="form-control" name="number_of_vehicles" min="0" step="1" v-model="feeWaiver.number_of_vehicles">
                        </div>
                    </div>
                </div>
            </div>
 
        </FormSection>

        <input type="button" @click.prevent="submit" class="btn btn-primary pull-right" value="Submit"/>
        <!--button v-else disabled class="btn btn-primary"><i class="fa fa-spin fa-spinner"></i>&nbsp;Submitting</button-->
    </div>
</template>

<script>

    /*
    import ComponentSiteSelection from '@/components/common/apiary/component_site_selection.vue'
    import FileField from '@/components/forms/filefield_immediate.vue'
    import SiteLocations from '@/components/common/apiary/site_locations.vue'
    import ApiaryChecklist from '@/components/common/apiary/section_checklist.vue'
    import uuid from 'uuid'
    import DeedPoll from "@/components/common/apiary/section_deed_poll.vue"
    */
    import { api_endpoints, helpers }from '@/utils/hooks'
    import FormSection from "@/components/forms/section_toggle.vue"
    import 'bootstrap/dist/css/bootstrap.css';
    import 'eonasdan-bootstrap-datetimepicker';
    require("select2/dist/css/select2.min.css");
    require("select2-bootstrap-theme/dist/select2-bootstrap.min.css");

    export default {
        name: 'FeeWaiverForm',
        props:{
            /*
            proposal:{
                type: Object,
                required:true
            },
            canEditActivities:{
              type: Boolean,
              default: true
            },
            is_external:{
              type: Boolean,
              default: false
            },
            is_internal:{
              type: Boolean,
              default: false
            },
            is_referral:{
              type: Boolean,
              default: false
            },
            hasReferralMode:{
                type:Boolean,
                default: false
            },
            hasAssessorMode:{
                type:Boolean,
                default: false
            },
            referral:{
                type: Object,
                required:false
            },
            proposal_parks:{
                type:Object,
                default:null
            },
            */
        },
        data:function () {
            let vm = this;
            return {
                feeWaiver: {},
                feeWaiverId: null,
                contactDetails: {},
                email_confirmation: '',
                participantGroupList: [],
                /*
                values:null,
                pBody: 'pBody'+vm._uid,
                component_site_selection_key: '',
                expiry_date_local: '',
                deed_poll_url: '',
                */
            }
        },
        components: {
            FormSection,
            /*
            SiteLocations,
            ComponentSiteSelection,
            FileField,
            ApiaryChecklist,
            DeedPoll,
            */
        },
        computed: {
            /*
            showActionAvailableUnavailable: function() {
                let show = false
                if(this.is_external){
                    if(this.proposal && ['approved', 'Approved'].includes(this.proposal.customer_status)){
                        show = true
                    }
                }
                return show
            },
            showColStatus: function() {
                let show = false

                show = true

                return show
            },
            apiary_sections_classname: function() {
                // For external page, we need 'col-md-9' classname
                // but not for the internal.
                // This is a hacky way, though...
                if(this.is_internal){
                    return ''
                } else {
                    return 'col-md-9'
                }
            },
            deedPollDocumentUrl: function() {
                let url = '';
                if (this.proposal && this.proposal.proposal_apiary) {
                    url = helpers.add_endpoint_join(
                        '/api/proposal_apiary/',
                        this.proposal.proposal_apiary.id + '/process_deed_poll_document/'
                    )
                }
                return url;
            },
            supportingApplicationDocumentUrl: function() {
                let url = '';
                if (this.proposal && this.proposal.proposal_apiary) {
                    url = helpers.add_endpoint_join(
                        '/api/proposal_apiary/',
                        this.proposal.proposal_apiary.id + '/process_supporting_application_document/'
                    )
                }
                return url;
            },
            publicLiabilityInsuranceDocumentUrl: function() {
                let url = '';
                if (this.proposal && this.proposal.proposal_apiary) {
                    url = helpers.add_endpoint_join(
                        '/api/proposal_apiary/',
                        this.proposal.proposal_apiary.id + '/process_public_liability_insurance_document/'
                    )
                }
                return url;
            },
            readonly: function() {
                let readonlyStatus = true;
                if (this.proposal.customer_status === 'Draft' && !this.is_internal) {
                    readonlyStatus = false;
                }
                return readonlyStatus;
            },
            assessorChecklistReadonly: function() {
                let readonlyStatus = true;
                //if (this.proposal.processing_status === 'With Assessor' && this.is_internal) {
                if (this.is_internal && this.proposal && this.proposal.assessor_mode && this.proposal.assessor_mode.assessor_can_assess) {
                    readonlyStatus = false;
                }
                return readonlyStatus;
            },
            assessorChecklistVisibility: function() {
                let visibility = false;
                //if (this.proposal.processing_status === 'With Assessor' && this.is_internal) {
                if (this.is_internal && this.proposal && this.proposal.assessor_mode && this.proposal.assessor_mode.has_assessor_mode) {
                    visibility = true;
                }
                return visibility;
            },
            referrerChecklistReadonly: function() {
                let readonlyStatus = true;
                // referrer must have access
                if (this.is_internal && this.proposal.processing_status === 'With Referral' &&
                    this.referral && this.referral.processing_status === 'Awaiting' &&
                    this.referral.apiary_referral && this.referral.apiary_referral.can_process) {
                    readonlyStatus = false;
                }
                return readonlyStatus;
            },
            referrerChecklistVisibility: function() {
                let visibility = false;
                // must be relevant referral
                if ((!this.referrerChecklistReadonly && r.id === this.referral.id) || this.assessorChecklistVisibility) {
                    visibility = true;
                }
                return visibility;
            },
            getUnansweredChecklistQuestions: function() {
                let UnansweredChecklistQuestions = false;

                if(this.applicantChecklistAnswers){
                    let numOfAnswers = this.applicantChecklistAnswers.length;
                    for( let i=0; i< numOfAnswers ; i ++){
                        if(this.applicantChecklistAnswers[i].answer == null && !this.applicantChecklistAnswers[i].text_answer){
                            UnansweredChecklistQuestions = true;
                        }
                    }
                }
                return UnansweredChecklistQuestions;
            },
            apiary_sites: function() {
                if (this.proposal && this.proposal.proposal_apiary) {
                    return this.proposal.proposal_apiary.apiary_sites;
                }
            },
            draftApiaryApplication: function() {
                let draftStatus = false;
                if (this.is_external && this.proposal && this.proposal.application_type === 'Apiary' && this.proposal.customer_status === 'Draft') {
                    draftStatus = true;
                }
                return draftStatus;
            },
            applicantChecklistAnswers: function() {
                if (this.proposal && this.proposal.proposal_apiary && this.proposal.proposal_apiary.applicant_checklist_answers &&
                    this.proposal.proposal_apiary.applicant_checklist_answers.length > 0) {
                    return this.proposal.proposal_apiary.applicant_checklist_answers;
                }
            },
            assessorChecklistAnswers: function() {
                if (this.proposal && this.proposal.proposal_apiary && this.proposal.proposal_apiary.assessor_checklist_answers &&
                    this.proposal.proposal_apiary.assessor_checklist_answers.length > 0) {
                    return this.proposal.proposal_apiary.assessor_checklist_answers;
                }
            },
            referrerChecklistAnswers: function() {
                if (this.proposal && this.proposal.proposal_apiary && this.proposal.proposal_apiary.referrer_checklist_answers &&
                    this.proposal.proposal_apiary.referrer_checklist_answers.length > 0) {
                    return this.proposal.proposal_apiary.referrer_checklist_answers;
                }
            },
            */
        },
        methods:{
            submit: async function(){
                console.log('in submit');

                //let vm = this;
                //vm.form=document.forms.new_proposal;
                //let formData = new FormData(vm.form);
                // Add apiary_sites data if needed
                //formData = this.attach_apiary_sites_data(formData)
                /*
                let missing_data = vm.can_submit();
                if(missing_data!=true){
                  swal({
                    title: "Please fix following errors before submitting",
                    text: missing_data,
                    type:'error'
                  })
                //vm.paySubmitting=false;
                return false;
                }

                var num_missing_fields = vm.validate()
                if (num_missing_fields > 0) {
                    vm.highlight_missing_fields()
                    var top = ($('#error').offset() || { "top": NaN }).top;
                    $('html, body').animate({
                        scrollTop: top
                    }, 1);
                    return false;
                }
                */
                // remove the confirm prompt when navigating away from window (on button 'Submit' click)
                //vm.submitting = true;
                let swalTitle = "Submit Request";
                let swalText = "Are you sure you want to submit this request?";
                /*
                if (this.apiaryTemplateGroup) {
                    swalTitle = "Submit Application";
                    swalText = "Are you sure you want to submit this application?";
                }
                */
                if (this.feeWaiver.date_from) {
                    this.feeWaiver.date_from = moment(this.feeWaiver.date_from, 'DD/MM/YYYY').format('YYYY-MM-DD');
                }
                if (this.feeWaiver.date_to) {
                    this.feeWaiver.date_to = moment(this.feeWaiver.date_to, 'DD/MM/YYYY').format('YYYY-MM-DD');
                }
                const payload = {
                    'contact_details': this.contactDetails,
                    'fee_waiver': this.feeWaiver,
                }
                await swal({
                    title: swalTitle,
                    text: swalText,
                    type: "question",
                    showCancelButton: true,
                    confirmButtonText: 'Submit'
                })
                const returnedFeeWaiver = await this.$http.post(api_endpoints.feewaivers,payload);
                console.log(returnedFeeWaiver);
                this.$router.push({
                    name: 'submit_feewaiver',
                    params: { fee_waiver: returnedFeeWaiver.body}
                });

                /*
                    .then(() => {
                    console.log('in then()');
                    vm.submittingProposal = true;
                    // Only Apiary has an application fee
                    if (!vm.proposal.fee_paid || ['Apiary', 'Site Transfer'].includes(vm.proposal.application_type)) {
                    //if (this.submit_button_text === 'Pay and submit' && ['Apiary', 'Site Transfer'].includes(vm.proposal.application_type)) {
                        vm.save_and_redirect();
                    } else {
                        //vm.save_wo_confirm()
                        vm.save(false)
                        vm.$http.post(helpers.add_endpoint_json(api_endpoints.proposals,vm.proposal.id+'/submit'),formData).then(res=>{
                            vm.proposal = res.body;
                            vm.$router.push({
                                name: 'submit_proposal',
                                params: { proposal: vm.proposal}
                            });
                        },err=>{
                            swal(
                                'Submit Error',
                                helpers.apiVueResourceError(err),
                                'error'
                            )
                        });
                    }
                },(error) => {
                  vm.paySubmitting=false;
                });
                //vm.submittingProposal= false;
                */
            },
            addEventListeners: function() {
              let vm = this;
              let el_fr_date = $(vm.$refs.dateFromPicker);
              let el_to_date = $(vm.$refs.dateToPicker);

              // "From" field
              el_fr_date.datetimepicker({
                format: "DD/MM/YYYY",
                minDate: "now",
                showClear: true
              });
              el_fr_date.on("dp.change", function(e) {
                if (el_fr_date.data("DateTimePicker").date()) {
                  vm.feeWaiver.date_from = e.date.format("DD/MM/YYYY");
                  el_to_date.data("DateTimePicker").minDate(e.date);
                } else if (el_fr_date.data("date") === "") {
                  vm.feeWaiver.date_from = "";
                }
              });

              // "To" field
              el_to_date.datetimepicker({
                format: "DD/MM/YYYY",
                //minDate: "now",
                //minDate: el_fr_date,
                showClear: true
              });
              el_to_date.on("dp.change", function(e) {
                if (el_to_date.data("DateTimePicker").date()) {
                  vm.feeWaiver.date_to = e.date.format("DD/MM/YYYY");
                } else if (el_to_date.data("date") === "") {
                  vm.feeWaiver.date_to = "";
                }
              });
                /*
              window.addEventListener('beforeunload', this.leaving);
              window.addEventListener('onblur', this.leaving);
              */
            },
            fetchParticipantsGroupList: async function() {
                //this.loading.push('Loading Apiary Referral Groups');
                this.participantGroupList = [];
                const response = await this.$http.get(api_endpoints.participants)
                for (let group of response.body) {
                    this.participantGroupList.push(group)
                }
                /*
                    this.loading.splice('Loading Apiary Referral Groups',1);
                },(error) => {
                    console.log(error);
                    this.loading.splice('Loading Apiary Referral Groups',1);
                })
                */

            },

            /*
            addEventListeners: function () {
                let vm = this;
                let el_fr = $(vm.$refs.expiryDatePicker);
                let options = {
                    format: "DD/MM/YYYY",
                    showClear: true ,
                    useCurrent: false,
                };

                el_fr.datetimepicker(options);

                el_fr.on("dp.change", function(e) {
                    if (e.date){
                        // Date selected
                        vm.expiry_date_local= e.date.format('DD/MM/YYYY')  // e.date is moment object
                    } else {
                        // Date not selected
                        vm.expiry_date_local = null;
                    }
                    vm.$emit('expiry_date_changed', vm.expiry_date_local)
                });

                //***
                // Set dates in case they are passed from the parent component
                //***
                let searchPattern = /^[0-9]{4}/

                let expiry_date_passed = vm.proposal.proposal_apiary.public_liability_insurance_expiry_date;
                console.log('passed')
                console.log(expiry_date_passed)
                if (expiry_date_passed) {
                    // If date passed
                    if (searchPattern.test(expiry_date_passed)) {
                        // Convert YYYY-MM-DD to DD/MM/YYYY
                        expiry_date_passed = moment(expiry_date_passed, 'YYYY-MM-DD').format('DD/MM/YYYY');
                    }
                    $('#expiry_date_input_element').val(expiry_date_passed);
                }
            },
            assessorChecklistAnswersPerSite: function(siteId) {
                let siteList = []
                if (this.proposal && this.proposal.proposal_apiary && this.proposal.proposal_apiary.assessor_checklist_answers_per_site &&
                    this.proposal.proposal_apiary.assessor_checklist_answers_per_site.length > 0) {
                    for (let answer of this.proposal.proposal_apiary.assessor_checklist_answers_per_site) {
                        if (answer.apiary_site_id === siteId) {
                            siteList.push(answer)
                        }
                    }
                }
                return siteList;
            },
            referrerChecklistAnswersPerSite: function(referralId, siteId) {
                let siteList = []
                if (this.proposal.proposal_apiary && this.proposal.proposal_apiary.referrer_checklist_answers_per_site) {
                    for (let referral of this.proposal.proposal_apiary.referrer_checklist_answers_per_site) {
                        if (referral.referral_data && referral.referral_data.length > 0) {
                            for (let answer of referral.referral_data) {
                                if (answer.site && answer.apiary_site_id === siteId && answer.apiary_referral_id === referralId) {
                                    siteList.push(answer)
                                }
                            }
                        }
                    }
                }
                console.log(siteList)
                return siteList;
            },

            num_of_sites_south_west_to_add_as_remainder: function(value){
                this.$emit('num_of_sites_south_west_to_add_as_remainder', value)
            },
            num_of_sites_remote_to_add_as_remainder: function(value){
                this.$emit('num_of_sites_remote_to_add_as_remainder', value)
            },
            num_of_sites_south_west_renewal_to_add_as_remainder: function(value){
                this.$emit('num_of_sites_south_west_renewal_to_add_as_remainder', value)
            },
            num_of_sites_remote_renewal_to_add_as_remainder: function(value){
                this.$emit('num_of_sites_remote_renewal_to_add_as_remainder', value)
            },
            button_text: function(button_text) {
                this.$emit('button_text', button_text)
            },
            total_fee_south_west: function(total_fee){
                this.$emit('total_fee_south_west', total_fee)
            },
            total_fee_remote: function(total_fee){
                this.$emit('total_fee_remote', total_fee)
            },
            total_fee_south_west_renewal: function(total_fee){
                this.$emit('total_fee_south_west_renewal', total_fee)
            },
            total_fee_remote_renewal: function(total_fee){
                this.$emit('total_fee_remote_renewal', total_fee)
            },
            num_of_sites_remain_south_west: function(value){
                this.$emit('num_of_sites_remain_south_west', value)
            },
            num_of_sites_remain_remote: function(value){
                this.$emit('num_of_sites_remain_remote', value)
            },
            num_of_sites_remain_south_west_renewal: function(value){
                this.$emit('num_of_sites_remain_south_west_renewal', value)
            },
            num_of_sites_remain_remote_renewal: function(value){
                this.$emit('num_of_sites_remain_remote_renewal', value)
            },
            remove_apiary_site: function(apiary_site_id){
                this.$refs.apiary_site_locations.removeApiarySiteById(apiary_site_id)
            },
            */

        },
        created: function() {
        },
        mounted: function() {
            //let vm = this;
            this.$nextTick(async () => {
            console.log("mounted")
            if (this.feeWaiverId) {
                console.log("mounted next")
                /*
                const url = helpers.add_endpoint_join(
                    api_endpoints.feewaivers,
                    this.feeWaiverId,
                    '/feewaiver_contactdetails_pack/'
                )
                */
                const url = api_endpoints.feewaivers + this.feeWaiverId + '/feewaiver_contactdetails_pack/';

                const returnVal = await this.$http.get(url);
                console.log(url);
                console.log(returnVal);
                /*
                this.contactDetails = returnVal.body.contact_details;
                this.feeWaiver = returnVal.body.fee_waiver;
                */
                //Object.assign(this.feeWaiver, returnVal.body);
                let feeWaiverUpdate = Object.assign({}, returnVal.body.fee_waiver)
                feeWaiverUpdate.date_to = moment(feeWaiverUpdate.date_to, 'YYYY-MM-DD').format('DD/MM/YYYY');
                feeWaiverUpdate.date_from = moment(feeWaiverUpdate.date_from, 'YYYY-MM-DD').format('DD/MM/YYYY');
                feeWaiverUpdate.number_of_vehicles = feeWaiverUpdate.number_of_vehicles.toString()
                this.feeWaiver = Object.assign({}, feeWaiverUpdate);

                this.contactDetails = Object.assign({}, returnVal.body.contact_details);
            }
                this.addEventListeners();
                this.fetchParticipantsGroupList();
            });
        },
        // this needs to go into the internal wrapper form, which will then pass feeWaiverId to this component as a prop
        beforeRouteEnter: function(to, from, next) {
            next(vm => {
                vm.feeWaiverId = to.params.fee_waiver_id;
            })
        }
    }
</script>

<style lang="css" scoped>
    .section{
        text-transform: capitalize;
    }
    .list-group{
        margin-bottom: 0;
    }
    .fixed-top{
        position: fixed;
        top:56px;
    }
    .insurance-items {
        padding-inline-start: 1em;
    }
    .my-container {
        display: flex;
        flex-direction: row;
        align-items: center;
    }
    .grow1 {
        flex-grow: 1;
    }
    .grow2 {
        flex-grow: 2;
    }
    .input-file-wrapper {
        margin: 1.5em 0 0 0;
    }
</style>

