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
                          <textarea class="form-control" v-model="contactDetails.organisation_description"/>
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
                        <label class="col-sm-4 control-label">Park/s</label>
                        <div class="col-sm-6">
                            <select ref="parks" class="form-control" multiple="multiple">
                                <option value="null"></option>
                                <option v-for="park in parksList" :value="park.id">{{park.name}}</option>
                            </select>
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
    require("select2");

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
                selectedParkIds: [],
            }
        },
        components: {
            FormSection,
        },
        computed: {
        },
        methods:{
            updateSelectedParks: function() {
                if (this.feeWaiver && this.feeWaiver.park_ids && this.feeWaiver.park_ids.length > 0) {
                    //this.selectedParkIds = [];
                    console.log(this.feeWaiver.park_ids);
                    $(this.$refs.parks).val(this.feeWaiver.park_ids);
                    $(this.$refs.parks).trigger('change');
                    /*
                    for (let parkId of this.feeWaiver.park_ids) {
                        this.selectedParkIds.push(parkId);
                        $(this.$refs.parks).val(parkId);
                    }
                    */
                }
            },
            submit: async function(){
                let swalTitle = "Submit Request";
                let swalText = "Are you sure you want to submit this request?";
                if (this.feeWaiver.date_from) {
                    this.feeWaiver.date_from = moment(this.feeWaiver.date_from, 'DD/MM/YYYY').format('YYYY-MM-DD');
                }
                if (this.feeWaiver.date_to) {
                    this.feeWaiver.date_to = moment(this.feeWaiver.date_to, 'DD/MM/YYYY').format('YYYY-MM-DD');
                }
                const payload = {
                    'contact_details': this.contactDetails,
                    'fee_waiver': this.feeWaiver,
                    'parks': this.selectedParkIds,
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
              // Parks multi select

              let el_parks = $(vm.$refs.parks);
              el_parks.select2();
              el_parks.on('select2:select', function(e) {
                  //console.log(e);
                  let val = e.params.data;
                  if (!vm.selectedParkIds.includes(val.id)) {
                      vm.selectedParkIds.push(val.id);
                  }
              }).
              on("select2:unselect",function (e) {
                  //console.log(e);
                  let val = e.params.data;
                  if (vm.selectedParkIds.includes(val.id)) {
                      let index = vm.selectedParkIds.indexOf(val.id);
                      vm.selectedParkIds.splice(index, 1);
                  }
              });

                /*
              window.addEventListener('beforeunload', this.leaving);
              window.addEventListener('onblur', this.leaving);
              */
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
        mounted: function() {
            //let vm = this;
            this.$nextTick(async () => {
                await this.fetchParticipantsGroupList();
                await this.fetchParksList();
                this.addEventListeners();
                if (this.feeWaiverId) {
                    console.log(this.feeWaiverId);
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
                    let feeWaiverUpdate = Object.assign({}, returnVal.body.fee_waiver);
                    feeWaiverUpdate.date_to = moment(feeWaiverUpdate.date_to, 'YYYY-MM-DD').format('DD/MM/YYYY');
                    feeWaiverUpdate.date_from = moment(feeWaiverUpdate.date_from, 'YYYY-MM-DD').format('DD/MM/YYYY');
                    feeWaiverUpdate.number_of_vehicles = feeWaiverUpdate.number_of_vehicles.toString()
                    this.feeWaiver = Object.assign({}, feeWaiverUpdate);

                    this.contactDetails = Object.assign({}, returnVal.body.contact_details);
                    // TODO: try to improve this
                    if (this.contactDetails.participants_code) {
                        this.contactDetails.participants_id = this.contactDetails.participants_code;
                    }
                    this.updateSelectedParks();
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

