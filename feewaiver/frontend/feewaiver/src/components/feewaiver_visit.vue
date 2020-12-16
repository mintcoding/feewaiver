<template lang="html">
            <FormSection :formCollapse="false" :label="label" :Index="'index_' + visit.index">
                <div class="col-sm-10">
                    <div class="form-group">
                        <div class="row">
                            <label for="visit_description" class="col-sm-4 control-label">Provide the details of your visit</label>
                            <div class="col-sm-8">
                                <textarea :disabled="readonly" required class="form-control" name="visit_description" v-model="visit.description"/>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="col-sm-10">
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
                <div v-if="isInternal" class="col-sm-10">
                    <div :key="feeWaiverId" class="form-group">
                        <div class="row">
                            <label class="col-sm-4">Applicable camping waiver</label>
                                <select :disabled="!canProcess" class="form-control" v-model="visit.camping_assessment">
                                    <option v-for="choice in campingChoices" :value="Object.keys(choice)[0]">{{Object.values(choice)[0]}}</option>
                                </select>
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
                            <label class="col-sm-4 control-label">Park/s</label>
                            <div class="col-sm-6">
                                <select :disabled="readonly" required :id="'parks_' + visit.index" class="form-control" multiple="multiple">
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
                                <input :disabled="readonly" required type="number" class="form-control" name="number_of_vehicles" min="0" step="1" v-model="visit.number_of_vehicles">
                            </div>
                        </div>
                    </div>
                    <div class="form-group">
                        <div class="row">
                            <label class="col-sm-4 control-label">Age of participants</label>
                            <div class="col-sm-8">
                            <input :disabled="readonly" type="checkbox" id="15" value="15" v-model="visit.age_of_participants_array">
                            <label>Under 15 yrs</label>
                            <input :disabled="readonly" type="checkbox" id="24" value="24" v-model="visit.age_of_participants_array">
                            <label>15-24 yrs</label>
                            <input :disabled="readonly" type="checkbox" id="25" value="25" v-model="visit.age_of_participants_array">
                            <label>25-39 yrs</label>
                            <input :disabled="readonly" type="checkbox" id="40" value="40" v-model="visit.age_of_participants_array">
                            <label>40-59 yrs</label>
                            <input :disabled="readonly" type="checkbox" id="60" value="60" v-model="visit.age_of_participants_array">
                            <label>60 yrs and over</label>
                            </div>
                        </div>
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
    require("select2");

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
            }
        },
        components: {
            FormSection,
        },
        computed: {
        },
        methods:{
            updateJqueryData: function() {
                // required when loading data from backend
                let vm = this;

                let el_parks = $('#parks_'+vm.visit.index)
                el_parks.val(vm.visit.selected_park_ids);
                el_parks.trigger('change');
                
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
              //let el_parks = $(vm.$refs.refLabel);
              let el_parks = $('#' + parkLabel);
              el_parks.select2();
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

