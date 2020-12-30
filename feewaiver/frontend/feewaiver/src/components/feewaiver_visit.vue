<template lang="html">
            <FormSection :formCollapse="false" :label="label" :Index="'index_' + visit.index" :noChevron="!isInternal" >
                <div class="col-sm-10">
                    <div class="form-group">
                        <div class="row">
                            <label for="visit_description" class="col-sm-4 control-label" >Provide the details of your visit</label>
                            <div class="col-sm-8">
                                <textarea 
                                    :disabled="readonly" 
                                    required 
                                    class="form-control" 
                                    name="visit_description" 
                                    v-model="visit.description"
                                    :id="'visit_description_' + visit.index"
                                />
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-sm-10">
                    <div class="form-group">
                        <div class="row">
                            <label class="col-sm-4 control-label">Park/s</label>
                            <div :id="'parks_parent_' + visit.index" class="col-sm-6">
                                <select :disabled="readonly" required :id="'parks_' + visit.index" class="form-control" multiple="multiple">
                                    <!--option value="null"></option-->
                                    <option v-for="park in parksList" :value="park.id">{{park.name}}</option>
                                </select>
                            </div>
                        </div>
                    </div>

                    <div class="form-group">
                        <div class="row">
                              <label class="col-sm-4">Are you intending to camp on CALM land during your visit?</label>
                                <input :disabled="readonly" class="col-sm-1" id="yes" type="radio" v-model="visit.camping_requested" v-bind:value="true">
                                <label class="col-sm-1" for="yes">Yes</label>
                                <input :disabled="readonly" class="col-sm-1" id="no" type="radio" v-model="visit.camping_requested" v-bind:value="false">
                                <label class="col-sm-1" for="no">No</label>
                        </div>
                    </div>
                </div>
                <div v-if="visit.camping_requested" class="col-sm-10">
                    <div v-if="isInternal" :key="feeWaiverId" class="form-group">
                        <div class="row">
                            <label class="col-sm-4">Applicable camping waiver</label>
                                <div class="col-sm-8">
                                    <select :disabled="!canProcess" class="form-control" v-model="visit.camping_assessment">
                                        <option v-for="choice in campingChoices" :value="Object.keys(choice)[0]">{{Object.values(choice)[0]}}</option>
                                    </select>
                                </div>
                        </div>
                    </div>
                    <div class="form-group">
                        <div class="row">
                            <label class="col-sm-4 control-label">Campground/s</label>
                            <div :id="'campgrounds_parent_' + visit.index" class="col-sm-6 campgroundclass">
                                <select :disabled="readonly" required :id="'campgrounds_' + visit.index" class="form-control" multiple="multiple">
                                    <!--option value="null"></option-->
                                    <option v-for="campground in selectableCampGrounds" :value="campground.id">{{campground.name}}</option>
                                </select>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-sm-10">
                    <div class="form-group">
                        <div class="row">
                            <label class="col-sm-4 control-label">Date from</label>
                            <div class="col-sm-4">
                                <div class="input-group date" :id="'dateFromPicker_' + visit.index">
                                        <input :disabled="readonly" required type="text" class="form-control" placeholder="DD/MM/YYYY" v-model="visit.date_from" />
                                        <span class="input-group-addon">
                                            <span class="glyphicon glyphicon-calendar"></span>
                                        </span>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="form-group">
                        <div class="row">
                            <label class="col-sm-4 control-label">Date to</label>
                            <div class="col-sm-4">
                                <div class="input-group date" :id="'dateToPicker_' + visit.index">
                                        <input :disabled="readonly" required type="text" class="form-control" placeholder="DD/MM/YYYY" v-model="visit.date_to" />
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
                                <input :disabled="readonly" required type="number" class="form-control" name="number_of_vehicles" min="0" step="1" v-model="visit.number_of_vehicles">
                            </div>
                        </div>
                    </div>
                    <div class="form-group">
                        <div class="row" >
                            <label class="col-sm-4 control-label">Age of participants</label>
                            <div class="col-sm-8">
                            <p>
                                <input :ref="'age_of_participants_' + visit.index" :disabled="readonly" type="checkbox" id="15" value="15" v-model="visit.age_of_participants_array">
                                <label>Under 15 yrs</label>
                                <input :disabled="readonly" type="checkbox" id="24" value="24" v-model="visit.age_of_participants_array">
                                <label>15-24 yrs</label>
                                <input :disabled="readonly" type="checkbox" id="25" value="25" v-model="visit.age_of_participants_array">
                                <label>25-39 yrs</label>
                                <input :disabled="readonly" type="checkbox" id="40" value="40" v-model="visit.age_of_participants_array">
                                <label>40-59 yrs</label>
                                <input :disabled="readonly" type="checkbox" id="60" value="60" v-model="visit.age_of_participants_array">
                                <label>60 yrs and over</label>
                            </p>
                            <p>
                                <span class="error" aria-live="polite">{{ ageOfParticipantsErrorText }}</span>
                            </p>
                            </div>
                        </div>
                    </div>
                    <div v-if="isInternal" class="pull-right">
                        <label>Issue?</label>
                        <input :disabled="readonly" type="checkbox" id="visit_issue" :value="true" v-model="visit.issued" @change.prevent="recalcVisits">
                    </div>
                </div>
            </FormSection>

</template>

<script>

    import { api_endpoints, helpers }from '@/utils/hooks'
    import FormSection from "@/components/forms/section_toggle.vue"
    import 'bootstrap/dist/css/bootstrap.css';
    import 'eonasdan-bootstrap-datetimepicker';
    require("select2/dist/css/select2.min.css");
    require("select2-bootstrap-theme/dist/select2-bootstrap.min.css");
    //require("select2");
    import select2 from "select2/dist/js/select2.full.js";

    export default {
        name: 'FeeWaiverVisit',
        props:{
            isInternal: {
                type: Boolean,
                default: false,
            },
            readonly: {
                type: Boolean,
                default: true,
            },
            visit:{
                type: Object,
                required:true
            },
            participantGroupList: {
                type: Array,
                required:true,
            },
            parksList: {
                type: Array,
                required:true,
            },
            campGroundsList: {
                type: Array,
                required:true,
            },
            campingChoices: {
                type: Array,
                required:true,
            },
            feeWaiverId:{
                type: String,
                //required: true,
            },
            canProcess:{
                type: Boolean,
                default: false,
            },
            Index: String,
            label: String,
        },
        data:function () {
            let vm = this;
            return {
                selectableCampGrounds: [],
            }
        },
        components: {
            FormSection,
        },
        computed: {
            ageOfParticipantsErrorText: function() {
                let errorText = "Please select at least one participant age group";
                if (this.visit && this.visit.age_of_participants_array && this.visit.age_of_participants_array.length > 0) {
                    errorText = '';
                }
                return errorText;
            },
            campingRequested: function() {
                return this.visit.camping_requested;
            },
            selectedParks: function() {
                return this.visit.selected_park_ids;
            },
        },
        watch: {
            campingRequested: {
                handler: async function(newVal, oldVal) {
                    if (newVal) {
                        await this.addCampGroundEventListener();
                    }
                },
                //deep: true
            },
            selectedParks: {
                handler: async function(newParks, oldParks) {
                    //await this.$nextTick();
                    //console.log(newParks);
                    await this.removeCampGroundEventListener();
                    this.selectableCampGrounds = [];
                    for (let campGround of this.campGroundsList) {
                        //console.log(campGround);
                        if (!campGround.park_id || newParks.includes(campGround.park_id.toString())) {
                        //if (!campGround.park_id) {
                            //console.log("push");
                            this.selectableCampGrounds.push(campGround);
                        }
                    }
                    await this.addCampGroundEventListener();
                },
                //deep: true
            },

        },

        methods:{
            recalcVisits: async function() {
                this.$emit('recalc-visits-flag');
            },
            updateJqueryData: function() {
                // required when loading data from backend
                let vm = this;

                // parks
                let el_parks = $('#parks_'+vm.visit.index)
                el_parks.val(vm.visit.selected_park_ids);
                el_parks.trigger('change');
                // campgrounds
                this.addCampGroundEventListener();
                let el_campgrounds = $('#campgrounds_'+vm.visit.index)
                el_campgrounds.val(vm.visit.selected_campground_ids);
                el_campgrounds.trigger('change');
                
                let el_fr_date = $('#dateFromPicker_' + vm.visit.index);
                el_fr_date.val(vm.visit.date_from);
                el_fr_date.trigger('change');
                let el_to_date = $('#dateToPicker_' + vm.visit.index);
                el_to_date.val(vm.visit.date_to);
                el_to_date.trigger('change');
            },
            addEventListeners: function() {
              let vm = this;
              // Parks multi select
              let el_fr_date = $('#dateFromPicker_' + vm.visit.index);
              let el_to_date = $('#dateToPicker_' + vm.visit.index);
              /*
              let el_fr_date = document.getElementById('dateFromPicker_' + i);
              let el_to_date = document.getElementById('dateToPicker_' + i);
              */

              // "From" field
              el_fr_date.datetimepicker({
                format: "DD/MM/YYYY",
                //minDate: "now",
                showClear: true
              });
              el_fr_date.on("dp.change", function(e) {
                if (el_fr_date.data("DateTimePicker").date()) {
                  vm.visit.date_from = e.date.format("DD/MM/YYYY");
                  el_to_date.data("DateTimePicker").minDate(e.date);
                } else if (el_fr_date.data("date") === "") {
                  vm.visit.date_from = "";
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
                  vm.visit.date_to = e.date.format("DD/MM/YYYY");
                } else if (el_to_date.data("date") === "") {
                  vm.visit.date_to = "";
                }
              });
              // Parks
              let parkLabel = 'parks_' + vm.visit.index;
              let parkParentLabel = 'parks_parent_' + vm.visit.index;
              //let el_parks = $(vm.$refs.refLabel);
              //$('#parks').css("z-index", 100000);
              let el_parks = $('#' + parkLabel);
                el_parks.select2({
                    /*
                    dropdownParent: $('#' + parkParentLabel),
                    selectionCssClass: "parkclass",
                    */
                    //containerCssClass: "parkclass",
                    placeholder: "parks",
                });
              //el_parks.css("z-index", 10);
              el_parks.on('select2:select', function(e) {
                  //console.log(e);
                  let val = e.params.data;
                  if (!vm.visit.selected_park_ids.includes(val.id)) {
                      vm.visit.selected_park_ids.push(val.id);
                  }
              }).
              on("select2:unselect",function (e) {
                  //console.log(e);
                  let val = e.params.data;
                  if (vm.visit.selected_park_ids.includes(val.id)) {
                      let index = vm.visit.selected_park_ids.indexOf(val.id);
                      vm.visit.selected_park_ids.splice(index, 1);
                  }
              });

            },
            addCampGroundEventListener: async function() {
              await this.$nextTick();
              let vm = this;
              // CampGrounds
              let campGroundLabel = 'campgrounds_' + vm.visit.index;
              let campGroundParentLabel = 'campgrounds_parent_' + vm.visit.index;
              let el_campgrounds = $('#' + campGroundLabel);
              $('.campgroundclass').css('z-index', 5);
              //console.log(el_campgrounds);
              el_campgrounds.select2({
                  /*
                  dropdownParent: $('#' + campGroundParentLabel),
                  selectionCssClass: "campgroundclass",
                  */
                  //containerCssClass: "campgroundclass",
                  placeholder: "campgrounds",
              });
              el_campgrounds.on('select2:select', function(e) {
                  //console.log(e);
                  let val = e.params.data;
                  if (!vm.visit.selected_campground_ids.includes(val.id)) {
                      vm.visit.selected_campground_ids.push(val.id);
                  }
              }).
              on("select2:unselect",function (e) {
                  //console.log(e);
                  let val = e.params.data;
                  if (vm.visit.selected_campground_ids.includes(val.id)) {
                      let index = vm.visit.selected_campground_ids.indexOf(val.id);
                      vm.visit.selected_campground_ids.splice(index, 1);
                  }
              });
            },
            removeCampGroundEventListener: async function() {
              await this.$nextTick();
              let vm = this;
              // CampGrounds
              let campGroundLabel = 'campgrounds_' + vm.visit.index;
              let el_campgrounds = $('#' + campGroundLabel);
              el_campgrounds.select2();
              el_campgrounds.off('select2:select').off("select2:unselect");
            },

        },

        created: function() {
        },
        mounted: function() {
            this.addEventListeners();
            this.updateJqueryData();
        },
    }
</script>

<style lang="css" scoped>
    .headerbox {
        padding: 50px;
    }
    .section{
        text-transform: capitalize;
    }
    .list-group{
        margin-bottom: 0;
    }
    /*
    .fixed-top{
        position: fixed;
        top:56px;
    }
    */
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
    /*
    .select2-container.parkclass {
        position: relative;
        z-index: 10;
    }
    .select2-container.campgroundclass {
        position: relative;
        z-index: 5;
    }
    .parkclass {
        z-index: 10;
    }
    .campgroundclass {
        z-index: 5;
    }
    */

</style>

