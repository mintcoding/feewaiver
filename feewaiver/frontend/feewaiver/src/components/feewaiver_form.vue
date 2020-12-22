<template lang="html">
    <div :class="containingClass">
        <!--strong> fill in form</strong-->
        <!--a class="navbar-brand" href="{% url 'ds_home' %}"><div style="inline"><img src="{% static 'feewaiver/img/dpaw_small.png' %}">Staff login</div></a-->
        <!--a class="navbar-brand pull-right" href="/"><div style="inline"><img src="/static/feewaiver/img/dpaw_small.png">Staff login</div></a-->
    <form id="feewaiver-form" @submit.prevent="submit">
        <div class="panel panel-default headerbox">
            <strong>
            Welcome to the Entry Fee Request Waiver form.

            Please fill out the details in the form below and submit the form to the Department.  You will be notified of the outcome of your request by email.
            </strong>
        </div>
        <FormSection :formCollapse="false" label="Contact Details" Index="contact_details">
            <div class="col-md-12">
                <div class="form-group">
                    <div class="row">
                    <label for="" class="col-sm-2 control-label">Organisation</label>
                    <div class="col-sm-4">
                        <input :disabled="readonly" required type="text" class="form-control" name="organisation" placeholder="" v-model="contactDetails.organisation">
                    </div>
                    <label for="" class="col-sm-2 control-label">Contact</label>
                    <div class="col-sm-4">
                        <input :disabled="readonly" required type="text" class="form-control" name="contact_name" placeholder="" v-model="contactDetails.contact_name">
                    </div>
                    </div>
                </div>
                <div class="form-group">
                    <div class="row">
                    <label for="" class="col-sm-2 control-label">Postal Address</label>
                    <div class="col-sm-4">
                        <input :disabled="readonly" required type="text" class="form-control" name="postal_address" placeholder="" v-model="contactDetails.postal_address">
                    </div>
                    </div>
                </div>
                <div class="form-group">
                    <div class="row">
                    <label for="suburb" class="col-sm-2 control-label">Suburb</label>
                    <div class="col-sm-4">
                        <input :disabled="readonly" required type="text" class="form-control" name="suburb" placeholder="" v-model="contactDetails.suburb">
                    </div>
                    <label for="state" class="col-sm-1 control-label">State</label>
                    <div class="col-sm-2">
                        <input :disabled="readonly" required type="text" class="form-control" name="state" placeholder="" v-model="contactDetails.state">
                    </div>
                    <label for="postcode" class="col-sm-1 control-label">Postcode</label>
                    <div class="col-sm-2">
                        <input :disabled="readonly" required type="text" class="form-control" name="postcode" placeholder="" v-model="contactDetails.postcode">
                    </div>
                    </div>
                </div>
                <div class="form-group">
                    <div class="row">
                    <label for="phone" class="col-sm-2 control-label">Phone</label>
                    <div class="col-sm-4">
                    <input :disabled="readonly" required type="text" class="form-control" name="phone" placeholder="" v-model="contactDetails.phone">
                    </div>
                    </div>
                </div>
                <div class="form-group">
                    <div class="row">
                        <label for="email" class="col-sm-2 control-label">Email</label>
                        <div class="col-sm-4">
                            <input :disabled="readonly" required type="email" class="form-control" name="email" placeholder="" v-model="contactDetails.email" id="contact_details_email">
                            <span class="error" aria-live="polite"></span>
                        </div>
                        <label for="email_confirmation" class="col-sm-2 control-label">Confirm Email</label>
                        <div class="col-sm-4">
                        <input :disabled="readonly" required type="email" class="form-control" name="email_confirmation" placeholder="" v-model="contactDetails.email_confirmation" id="email_confirmation">
                        </div>
                    </div>
                </div>
                <div class="form-group">
                    <div class="row">
                        <label class="col-sm-4 control-label">Participants</label>
                        <div class="col-sm-6">
                            <select :disabled="readonly" required ref="participants" class="form-control" v-model="contactDetails.participants_id">
                                <option value=""></option>
                                <option v-for="group in participantGroupList" :value="group.id">{{group.name}}</option>
                            </select>
                        </div>
                    </div>
                </div>
                <div class="form-group">
                    <div class="row">
                      <label class="col-sm-4 control-label">Provide a brief explanation of your organisation</label>
                      <div class="col-sm-8">
                          <textarea :disabled="readonly" required class="form-control" v-model="contactDetails.organisation_description"/>
                      </div>
                    </div>
                </div>
                <div class="form-group">
                    <div class="row">
                      <label class="col-sm-4 control-label">Attach any other documentation you want to provide</label>
                      <div class="col-sm-8">
                          <FileField
                              class="input_file_wrapper"
                              ref="contact_details_documents"
                              name="contact-details-documents"
                              :isRepeatable="true"
                              :documentActionUrl="documentActionUrl"
                              :replace_button_by_text="true"
                              @update-temp-doc-coll-id="updateTempDocCollId"
                              :key="documentActionUrl"
                              :readonly="readonly"
                          />
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
                          <textarea :disabled="readonly" required class="form-control" name="fee_waiver_purpose" v-model="feeWaiver.fee_waiver_purpose"/>
                      </div>
                    </div>
                </div>
            </div>
        </FormSection>
        <div v-for="visit in visits" :key="visit.id">
            <VisitSection 
            :formCollapse="false" 
            :label="'Visit ' + (visit.index + 1)"
            :Index="'index_' + visit.index"
            :ref="'visit_' + visit.index"
            :visit="visit"
            :participantGroupList="participantGroupList"
            :parksList="parksList"
            :campingChoices="campingChoices"
            :feeWaiverId="feeWaiverId"
            :canProcess="canProcess"
            :isInternal="isInternal"
            :readonly="readonly"
             @recalc-visits-flag="recalcVisitsFlag"
            />
        </div>
        <div v-if="isInternal">
            <FormSection :formCollapse="false" label="Comments to applicant" :Index="'comments_to_applicant' + feeWaiverId">
                <div class="form-group">
                    <div class="row">
                      <label class="col-sm-4 control-label">Comments</label>
                      <div class="col-sm-8">
                          <textarea :disabled="readonly" class="form-control" v-model="feeWaiver.comments_to_applicant"/>
                      </div>
                    </div>
                </div>
            </FormSection>
        </div>
        <div>
            <input type="hidden" name="csrfmiddlewaretoken" :value="csrf_token"/>
            <!--input type='hidden' name="schema" :value="JSON.stringify(proposal)" /-->
            <!--input type='hidden' name="proposal_id" :value="1" /-->
            <div class="row" style="margin-bottom: 50px">
              <div class="navbar navbar-fixed-bottom" style="background-color: #f5f5f5;">
                <div class="navbar-inner">
                    <div v-if="feeWaiverId" class="container">
                      <p class="pull-right">
                        <button class="btn btn-primary pull-right" style="margin-top:5px;" @click.prevent="save()">Save Changes</button>
                      </p>
                    </div>
                    <div v-else class="container">
                      <p class="pull-right">
                        <input type="button" @click.prevent="addVisit" class="btn btn-primary" value="Add another visit"/>
                        <button class="btn btn-primary" type="submit">Submit</button>
                      </p>
                    </div>
                </div>
              </div>
            </div>

        </div>

    </form>
    </div>
</template>

<script>

    import { api_endpoints, helpers }from '@/utils/hooks'
    import FormSection from "@/components/forms/section_toggle.vue"
    import 'bootstrap/dist/css/bootstrap.css';
    import 'eonasdan-bootstrap-datetimepicker';
    require("select2/dist/css/select2.min.css");
    require("select2-bootstrap-theme/dist/select2-bootstrap.min.css");
    require("select2");
    import VisitSection from "./feewaiver_visit.vue"
    import FileField from '@/components/forms/filefield_immediate.vue'

    export default {
        name: 'FeeWaiverForm',
        props:{
            feeWaiverId:{
                type: String,
                //required: true,
            },
            isFinalised:{
                type: Boolean,
                //required: true,
            },
            isInternal: {
                type: Boolean,
                default: false,
            },
            canProcess:{
                type: Boolean,
                default: false,
            },
        },
        data:function () {
            let vm = this;
            return {
                feeWaiver: {},
                payload: {},
                //allVisitsUnchecked: false,
                //feeWaiverId: null,
                contactDetails: {},
                //email_confirmation: '',
                participantGroupList: [],
                temporary_document_collection_id: null,
                parksList: [],
                campingChoices: [],
                //selected_park_ids: [],
                visitIdx: 0,
                visits: [
                    {
                        index: 0,
                        selected_park_ids: [],
                        age_of_participants_array: [],
                        camping_requested: false,
                    },
                ],
            }
        },
        components: {
            FormSection,
            VisitSection,
            FileField,
        },
        watch: {
            feeWaiver: {
                handler: function() {
                },
                deep: true
            },
        },
        computed: {
            /*
            canProcess: function() {
                let process = false;
                if (this.feeWaiver && this.feeWaiver.can_process) {
                    process = true;
                }
                return process;
            },
            */
            readonly: function() {
                if (this.isFinalised) {
                    return true
                } else if (this.isInternal) {
                    return !this.canProcess;
                } else {
                    return false;
                }
            },
            csrf_token: function() {
              return helpers.getCookie('csrftoken')
            },
            containingClass: function() {
                let cclass = 'container';
                if (this.feeWaiverId) {
                    //cclass = 'col-sm-12';
                    cclass = '';
                }
                console.log(cclass);
                return cclass;
            },
            documentActionUrl: function() {
                let url = '';
                if (this.contactDetails && this.contactDetails.id) {
                    url = helpers.add_endpoint_join(
                        '/api/feewaivers/',
                        //this.contactDetails.id + '/process_contact_details_document/'
                        this.feeWaiver.id + '/process_contact_details_document/'
                    )
                } else if (!this.feeWaiverId) {
                    // internal view
                    url = 'temporary_document';
                }
                return url;
            },

            // need temp doc
            /*
            let rendererDocumentUrl = helpers.add_endpoint_join(
                api_endpoints.call_email,
                state.call_email.id + "/process_renderer_document/"
                )
            //Vue.set(state.call_email, 'rendererDocumentUrl', rendererDocumentUrl); 
            let commsLogsDocumentUrl = helpers.add_endpoint_join(
                api_endpoints.call_email,
                state.call_email.id + "/process_comms_log_document/"
                )
            //Vue.set(state.call_email, 'commsLogsDocumentUrl', commsLogsDocumentUrl); 
            documentActionUrl: function() {
                let rendererDocumentUrl = '';
                if (this.call_email && this.call_email.id) {
                    rendererDocumentUrl = this.call_email.rendererDocumentUrl;
                } else if (this.inspection && this.inspection.id) {
                    rendererDocumentUrl = this.inspection.rendererDocumentUrl;
                } else if (this.physical_artifact && this.physical_artifact.id) {
                    rendererDocumentUrl = this.physical_artifact.rendererDocumentUrl;
                }
                return rendererDocumentUrl;
            },

            */
        },
        methods:{
            recalcVisitsFlag: async function() {
                let allVisitsUnchecked = true;
                await this.$nextTick();
                this.allVisitsUnchecked = true;
                for (let visit of this.visits) {
                    if (visit.issued) {
                        allVisitsUnchecked = false;
                    }
                }
                this.$emit('all-visits-unchecked', allVisitsUnchecked);
            },
            updateTempDocCollId: function(id) {
                this.temporary_document_collection_id = id.temp_doc_id;
            },
            addVisit: function() {
                /*
                let visit = {};
                visit.index = ++this.visitIdx;
                //visit.selected_park_ids = [];
                this.$set(visit, selected_park_ids, []);
                */
                let visit = {
                    index: ++this.visitIdx,
                    selected_park_ids: [],
                    age_of_participants_array: [],
                    camping_requested: false,
                }

                this.visits.push(visit);
            },
            /*
            checkBlankFields: function() {
                let blankFields = []

                if (!this.contactDetails.email) {
                    blankFields.push(' You must select..')
                }
                return blankFields
            },
            highlightMissingFields: function(){
                //let vm = this;
                for (let missingField of vm.missingFields) {
                    $("#" + missingField.id).css("color", 'red');
                }
            },
            */

            addEventListeners: function() {
                let vm = this;
                const contactDetailsEmail = document.getElementById('contact_details_email');
                const emailConfirmation = document.getElementById('email_confirmation');
                const emailError = document.querySelector('#contact_details_email + span.error');
                /*
                console.log(contactDetailsEmail);
                console.log(emailError);
                */
                contactDetailsEmail.addEventListener('input', function(evt) {
                    //console.log("contactDetailsEmail evt");
                    if (contactDetailsEmail.validity.valid) {
                        emailError.textContent = '';
                        emailError.className = 'error';
                    } else {
                        showEmailError();
                        /*
                        emailError.textContent = 'fix it';
                        emailError.className = 'error active';
                        */
                    }
                });
                contactDetailsEmail.onpaste = e => {
                    e.preventDefault();
                    return false;
                };
                emailConfirmation.onpaste = e => {
                    e.preventDefault();
                    return false;
                };
                contactDetailsEmail.onblur = e => {
                    //e.preventDefault();
                    //return false;
                    showEmailError();
                };
                emailConfirmation.onblur = e => {
                    //e.preventDefault();
                    showEmailError();
                    //return false;
                };
                const form = document.getElementsByTagName('form')[0]
                form.addEventListener('submit', function(evt) {
                    console.log(!vm.contactDetails.email);
                    console.log(!contactDetailsEmail.validity.valid) 
                    //if (!contactDetailsEmail.validity.valid || !vm.contactDetails.email) {
                    if (!contactDetailsEmail.validity.valid) {
                        showEmailError();
                        /*
                        emailError.textContent = 'fix it';
                        emailError.className = 'error active';
                        */
                        evt.preventDefault();
                    }
                });
                function showEmailError() {
                    console.log("show error")
                    if (contactDetailsEmail.validity.valueMissing || !vm.contactDetails.email) {
                        emailError.textContent = 'You need to enter an email address';
                    } else if (contactDetailsEmail.validity.typeMismatch) {
                        emailError.textContent = 'Entered value needs to be an email address';
                    } else if (vm.contactDetails.email && vm.contactDetails.email_confirmation && vm.contactDetails.email !== vm.contactDetails.email_confirmation) {
                        emailError.textContent = 'Email addresses are not identical';
                    }
                    emailError.className = 'error active';
                }

            },
            submit: async function(){
                let visitRef = null;
                let ageOfParticipants = null;
                for (let visit of this.visits) {
                    if (visit && visit.age_of_participants_array && visit.age_of_participants_array.length < 1) {
                        const visitIdx = 'visit_' + visit.index;
                        const ageOfParticipantsIdx = 'age_of_participants_' + visit.index
                        visitRef = this.$refs[visitIdx];
                        ageOfParticipants = visitRef[0].$refs[ageOfParticipantsIdx];
                    }
                }
                const contactDetailsEmail = document.getElementById('contact_details_email');
                if (!contactDetailsEmail.validity.valid || this.contactDetails.email !== this.contactDetails.email_confirmation) {
                    contactDetailsEmail.focus();
                } else if (ageOfParticipants) {
                    ageOfParticipants.focus();
                } else {
                    let swalTitle = "Submit Request";
                    let swalText = "Are you sure you want to submit this request?";
                    await this.updatePayload();
                    await swal({
                        title: swalTitle,
                        text: swalText,
                        type: "question",
                        showCancelButton: true,
                        confirmButtonText: 'Submit'
                    });
                    //console.log(this.payload)
                    const returnedFeeWaiver = await this.$http.post(api_endpoints.feewaivers,this.payload);
                    this.$router.push({
                        name: 'submit_feewaiver',
                        params: { fee_waiver: returnedFeeWaiver.body}
                    });
                }
            },
            updatePayload: async function() {
                await this.$nextTick();
                //await this.$nextTick(() => {
                this.payload = {};
                this.payload = {
                    'contact_details': Object.assign({}, this.contactDetails),
                    'fee_waiver': Object.assign({}, this.feeWaiver),
                    //'parks': this.selected_park_ids,
                    'visits': [],
                    'temporary_document_collection_id': this.temporary_document_collection_id,
                }
                for (let visitData of this.visits) {
                    let visit = Object.assign({}, visitData);
                    // convert date strings
                    if (visit.date_from) {
                        visit.date_from = moment(visit.date_from, 'DD/MM/YYYY').format('YYYY-MM-DD');
                    }
                    if (visit.date_to) {
                        visit.date_to = moment(visit.date_to, 'DD/MM/YYYY').format('YYYY-MM-DD');
                    }
                    // add to payload
                    this.payload.visits.push(visit)
                }
                //});
            },
            save: async function(confirmSave=true) {
                //await this.$nextTick(async () => {
                //let payload = {}
                await this.updatePayload()
                let url = `/api/feewaivers/${this.feeWaiverId}/assessor_save/`;
                //await this.$http.post(url, JSON.stringify(payload));
                //console.log("this.payload")
                //console.log(this.payload)
                const feeWaiverRes = await this.$http.post(url, this.payload);
                //console.log(feeWaiverRes);
                if (confirmSave) {
                    swal(
                        'Saved',
                        'Fee Waiver has been saved',
                        'success'
                    );
                }
                return feeWaiverRes
            },

            fetchParticipantsGroupList: async function() {
                this.participantGroupList = [];
                const response = await this.$http.get(api_endpoints.participants)
                for (let group of response.body) {
                    this.participantGroupList.push(group)
                }
            },
            fetchParksList: async function() {
                this.parksList = [];
                const response = await this.$http.get(api_endpoints.parks)
                for (let group of response.body) {
                    this.parksList.push(group)
                }
            },
            fetchCampingChoices: async function() {
                console.log("camping choices")
                this.campingChoices = [];
                const response = await this.$http.get(api_endpoints.camping_choices)
                for (let choice of response.body) {
                    this.campingChoices.push(choice)
                }
            },
            loadFeeWaiverData: async function() {
                await this.fetchCampingChoices();
                console.log(this.feeWaiverId);
                const url = api_endpoints.feewaivers + this.feeWaiverId + '/feewaiver_contactdetails_pack/';

                const returnVal = await this.$http.get(url);
                //console.log(url);
                console.log(returnVal.body.fee_waiver);
                this.feeWaiver.id = returnVal.body.fee_waiver.id;
                this.feeWaiver.lodgement_number = returnVal.body.fee_waiver.lodgement_number;
                this.feeWaiver.fee_waiver_purpose = returnVal.body.fee_waiver.fee_waiver_purpose;
                this.feeWaiver.comments_to_applicant = returnVal.body.fee_waiver.comments_to_applicant;
                this.feeWaiver.assigned_officer = returnVal.body.fee_waiver.assigned_officer;
                this.feeWaiver.assigned_officer_id = returnVal.body.fee_waiver.assigned_officer_id;
                this.feeWaiver.can_process = returnVal.body.fee_waiver.can_process;
                // visits should be empty if reading from backend
                this.visits = []
                this.visitIdx = -1;
                for (let retrievedVisit of returnVal.body.fee_waiver.visits) {
                    let visit = Object.assign({}, retrievedVisit);
                    //visit.index = visit.id;
                    visit.index = ++this.visitIdx;
                    visit.date_to = moment(visit.date_to, 'YYYY-MM-DD').format('DD/MM/YYYY');
                    visit.date_from = moment(visit.date_from, 'YYYY-MM-DD').format('DD/MM/YYYY');
                    visit.number_of_vehicles = visit.number_of_vehicles.toString()
                    //this.feeWaiver = Object.assign({}, feeWaiverUpdate);
                    this.visits.push(visit);
                }
                this.contactDetails = Object.assign({}, returnVal.body.contact_details);
                // TODO: try to improve this
                if (this.contactDetails.participants_code) {
                    this.contactDetails.participants_id = this.contactDetails.participants_code;
                }
            },

        },
        created: function() {
        },
        mounted: async function() {
            //let vm = this;
            await this.$nextTick(async () => {
                this.addEventListeners();
                await this.fetchParticipantsGroupList();
                await this.fetchParksList();
                if (this.feeWaiverId) {
                    await this.loadFeeWaiverData();
                    await this.recalcVisitsFlag();
                    /*
                    await this.fetchCampingChoices();
                    console.log(this.feeWaiverId);
                    const url = api_endpoints.feewaivers + this.feeWaiverId + '/feewaiver_contactdetails_pack/';

                    const returnVal = await this.$http.get(url);
                    //console.log(url);
                    //console.log(returnVal);
                    this.feeWaiver.id = returnVal.body.fee_waiver.id;
                    this.feeWaiver.lodgement_number = returnVal.body.fee_waiver.lodgement_number;
                    this.feeWaiver.fee_waiver_purpose = returnVal.body.fee_waiver.fee_waiver_purpose;
                    // visits should be empty if reading from backend
                    this.visits = []
                    this.visitIdx = -1;
                    for (let retrievedVisit of returnVal.body.fee_waiver.visits) {
                        let visit = Object.assign({}, retrievedVisit);
                        //visit.index = visit.id;
                        visit.index = ++this.visitIdx;
                        visit.date_to = moment(visit.date_to, 'YYYY-MM-DD').format('DD/MM/YYYY');
                        visit.date_from = moment(visit.date_from, 'YYYY-MM-DD').format('DD/MM/YYYY');
                        visit.number_of_vehicles = visit.number_of_vehicles.toString()
                        //this.feeWaiver = Object.assign({}, feeWaiverUpdate);
                        this.visits.push(visit);
                    }
                    this.contactDetails = Object.assign({}, returnVal.body.contact_details);
                    // TODO: try to improve this
                    if (this.contactDetails.participants_code) {
                        this.contactDetails.participants_id = this.contactDetails.participants_code;
                    }
                    */
                }
            });
        },
        /*
        // this needs to go into the internal wrapper form, which will then pass feeWaiverId to this component as a prop
        beforeRouteEnter: function(to, from, next) {
            next(vm => {
                vm.feeWaiverId = to.params.fee_waiver_id;
            })
        }
        */
    }
</script>

<!--style lang="css" scoped-->
<style lang="css">
/*
    input:required {
        border: 1px solid red;
    }
    select:required {
        border: 1px solid red;
    }
    .select2 {
        border: 1px solid red;
    }
    textarea:required {
        border: 1px solid red;
    }
    .actionBtn {
        cursor: pointer;
    }
    */
    .input_file_wrapper {
        margin: 1.5em 0 0 0;
    }
    .headerbox {
        padding: 50px;
    }
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
    .error {
        color: red;
    }
    /*
    input[type=email]{
        -webkit-appearance: none;
        appearance: none;

        width: 100%;
        border: 1px solid #333;
        margin: 0;

        font-family: inherit;
        font-size: 90%;

        box-sizing: border-box;
    }
    */
/*
    input[type=email]:invalid{
        border-color: #900;
        background-color: #FDD;
    }
    input:focus:invalid {
        outline: none;
    }
    */
</style>

