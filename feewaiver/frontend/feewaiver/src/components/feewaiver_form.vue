<template lang="html">
    <div class="container">
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
                        <input required type="text" class="form-control" name="organisation" placeholder="" v-model="contactDetails.organisation">
                    </div>
                    <label for="" class="col-sm-2 control-label">Contact</label>
                    <div class="col-sm-4">
                        <input required type="text" class="form-control" name="contact_name" placeholder="" v-model="contactDetails.contact_name">
                    </div>
                    </div>
                </div>
                <div class="form-group">
                    <div class="row">
                    <label for="" class="col-sm-2 control-label">Postal Address</label>
                    <div class="col-sm-4">
                        <input required type="text" class="form-control" name="postal_address" placeholder="" v-model="contactDetails.postal_address">
                    </div>
                    </div>
                </div>
                <div class="form-group">
                    <div class="row">
                    <label for="suburb" class="col-sm-2 control-label">Suburb</label>
                    <div class="col-sm-4">
                        <input required type="text" class="form-control" name="suburb" placeholder="" v-model="contactDetails.suburb">
                    </div>
                    <label for="state" class="col-sm-1 control-label">State</label>
                    <div class="col-sm-2">
                        <input required type="text" class="form-control" name="state" placeholder="" v-model="contactDetails.state">
                    </div>
                    <label for="postcode" class="col-sm-1 control-label">Postcode</label>
                    <div class="col-sm-2">
                        <input required type="text" class="form-control" name="postcode" placeholder="" v-model="contactDetails.postcode">
                    </div>
                    </div>
                </div>
                <div class="form-group">
                    <div class="row">
                    <label for="phone" class="col-sm-2 control-label">Phone</label>
                    <div class="col-sm-4">
                    <input required type="text" class="form-control" name="phone" placeholder="" v-model="contactDetails.phone">
                    </div>
                    </div>
                </div>
                <div class="form-group">
                    <div class="row">
                    <label for="email" class="col-sm-2 control-label">Email</label>
                    <div class="col-sm-4">
                        <input required type="text" class="form-control" name="email" placeholder="" v-model="contactDetails.email">
                    </div>
                    <label for="email_confirmation" class="col-sm-2 control-label">Confirm Email</label>
                    <div class="col-sm-4">
                    <input required type="text" class="form-control" name="email_confirmation" placeholder="" v-model="email_confirmation">
                    </div>
                    </div>
                </div>
                <div class="form-group">
                    <div class="row">
                        <label class="col-sm-4 control-label">Participants</label>
                        <div class="col-sm-6">
                            <select required ref="participants" class="form-control" v-model="contactDetails.participants_id">
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
                          <textarea required class="form-control" v-model="contactDetails.organisation_description"/>
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
                          <textarea required class="form-control" name="fee_waiver_purpose" v-model="feeWaiver.fee_waiver_purpose"/>
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
            />
        </div>

        <button class="btn btn-primary pull-right" type="submit">Submit</button>
        <!--input type="button" @click="submit" class="btn btn-primary pull-right" value="Submit"/-->
        <input type="button" @click.prevent="addVisit" class="btn btn-primary pull-right" value="Add another visit"/>
        <!--button v-else disabled class="btn btn-primary"><i class="fa fa-spin fa-spinner"></i>&nbsp;Submitting</button-->
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
                parksList: [],
                //selected_park_ids: [],
                visitIdx: 0,
                visits: [
                    {
                        index: 0,
                        selected_park_ids: [],
                        age_of_participants_array: [],
                    },
                ],
            }
        },
        components: {
            FormSection,
            VisitSection,
        },
        computed: {
        },
        methods:{
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
                }

                this.visits.push(visit);
            },
            checkBlankFields: function() {
                //let vm=this;
                let blankFields = []
                /*
                if (!(this.$refs.apiary_site_transfer.num_of_sites_selected > 0)){
                    blank_fields.push(' You must select at least one site to transfer')
                }
                */

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

            submit: async function(){
                /*
                let missingData = this.checkBlankFields();
                if(missingData.length > 0){
                  swal({
                    title: "Please fix following errors before submitting",
                    text: missingData,
                    type:'error'
                  })
                //return false;
                }
                */

                let swalTitle = "Submit Request";
                let swalText = "Are you sure you want to submit this request?";
                let payload = {
                    'contact_details': this.contactDetails,
                    'fee_waiver': this.feeWaiver,
                    //'parks': this.selected_park_ids,
                    'visits': [],
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
                    payload.visits.push(visit)
                }

                await swal({
                    title: swalTitle,
                    text: swalText,
                    type: "question",
                    showCancelButton: true,
                    confirmButtonText: 'Submit'
                })
                const returnedFeeWaiver = await this.$http.post(api_endpoints.feewaivers,payload);
                this.$router.push({
                    name: 'submit_feewaiver',
                    params: { fee_waiver: returnedFeeWaiver.body}
                });

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
        },
        created: function() {
        },
        mounted: async function() {
            //let vm = this;
            await this.$nextTick(async () => {
                await this.fetchParticipantsGroupList();
                await this.fetchParksList();
                if (this.feeWaiverId) {
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
                }
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
    */
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
</style>

