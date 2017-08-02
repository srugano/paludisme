'use strict';

/**
 * Add custom date formats 
 */
Highcharts.dateFormats = {
    W: function (timestamp) {
        var date = new Date(timestamp),
      day = date.getUTCDay() == 0 ? 7 : date.getUTCDay(),
      dayNumber;
    date.setDate(date.getUTCDate() + 4 - day);
    dayNumber = Math.floor((date.getTime() - new Date(date.getUTCFullYear(), 0, 1, -6)) / 86400000);
    return 1 + Math.floor(dayNumber / 7);
        
    }
}

$(document).ready(function() {

    var url =  "/stock/casespalus/?";
    $.getJSON(url, function(data) {
        // var raba = data;
        // var seriesData = [];
        // var xCategories = [];
        // var i, cat;
        // for(i = 0; i < data.length; i++){
        //      cat = data[i].unique();
        //      if(xCategories.indexOf(cat) === -1){
        //         xCategories[xCategories.length] = cat;
        //      }
        //      console.log(cat);
        // }
        // for(i = 0; i < data.length; i++){
        //     if(seriesData){
        //       var currSeries = seriesData.filter(function(seriesObject){ return seriesObject.name == data[i].status;});
        //       if(currSeries.length === 0){
        //           currSeries = seriesData[seriesData.length] = {name: data[i].status, data: []};
        //       } else {
        //           currSeries = currSeries[0];
        //       }
        //       var index = currSeries.data.length;
        //       currSeries.data[index] = data[i].val;
        //     } else {
        //        seriesData[0] = {name: data[i].status, data: [data[i].val]}
        //     }
        // }
        var lookup = {};
        var items = data;
        var simples = [];
        var acutes = [];
        var pregnant_womens = [];
        var deceases = [];

        for (var item, i = 0; item = items[i++];) {
          var simple = item.simple;
          var acute = item.acute;
          var pregnant_women = item.pregnant_women;
          var decease = item.decease;

          if (!(simple in lookup)) {
            lookup[simple] = 1;
            simples.push([Date.parse(item.week),simple]);
            lookup[acute] = 1;
            acutes.push([Date.parse(item.week), acute]);
            lookup[pregnant_women] = 1;
            pregnant_womens.push([Date.parse(item.week),pregnant_women]);
            lookup[decease] = 1;
            deceases.push([Date.parse(item.week),decease]);
          }
        }
        var seriesData = [{name: 'Simple', data:simples}, {name: 'Acute', data: acutes }, {name:"Pregnant women", data: pregnant_womens}, {name: "Decease", data:deceases}];
        var chart = new Highcharts.chart(
          'situation_cas_palu', 
          {
             chart: {
                type: 'spline'
            },
            title: {
                text: 'Nombres de cas de paludisme'
            },
            tooltip: {
                headerFormat: '<b>{series.name}</b><br>',
                pointFormat: '{point.x:%e. %b}: {point.y:.2f} cas'
            },
            xAxis:
              { 
                type: 'datetime',
                tickInterval: 7 * 24 * 36e5, // one week
                title: {
                    text: 'Date'
                },
                labels: {
                    format: '{value:Week %W/%Y}',
                    align: 'right',
                    rotation: -30
                }
              },
            yAxis: {
                title: {
                    text: 'Cas de paludisme'
                },
                min: 0
            },
            plotOptions: {
              spline: {
                  marker: {
                      enabled: true
                  }
              }
            }, 
            dateFormat: "YYYY-mm-dd",
            series: seriesData
          }
        );
      });
});

var app = angular.module('PaludismeApp', ['ngSanitize', 'datatables', 'datatables.buttons']);

app.controller('FilterCtrl', ['$scope', '$http', function($scope, $http) {

        // province
        $http.get("/bdiadmin/province/")
        .then(function (response) {
            if (response.data.length > 0) {
                $scope.provinces = response.data;
            } else {
                $("#province-group").hide();
                $http.get("/bdiadmin/district/")
                .then(function (response) {
                    $scope.districts = response.data;
                });
            }
        });
        // province
        $http.get("/stock/products/")
        .then(function (response) {
            if (response.data.length > 0) {
                $scope.products = response.data;
            } else {
                $("#province-group").hide();
                $http.get("/bdiadmin/district/")
                .then(function (response) {
                    $scope.districts = response.data;
                });
            }
        });
        $scope.update_province = function () {
            var province = $scope.province;
            if (province) {
              $http.get("/bdiadmin/district/?province=" + province.id)
              .then(function (response) {
                $scope.districts = response.data;
            });
            $http.get("/stock/casespalus/?report__facility__district__province=" + province.id)
              .then(function (response) {
                console.log(response.data);
            });
          }
      };
          // district
          $scope.update_district = function () {
            var district = $scope.district;
            if (district) {
              $http.get("/bdiadmin/cds/?district=" + district.id)
              .then(function (response) {
                  $scope.cdss = response.data;
              });
          }
      };
        // CDS
        $scope.update_cds = function () {
            var cds = $scope.cds;
            if (cds) {
              $http.get("/bdiadmin/cds/" + cds.id + "/" )
              .then(function (response) {
                  $scope.etablissements = response.data;
              });
      }
    };
    // CDS
        $scope.update_product = function () {
            var product = $scope.product;
            if (product) {
              $http.get("/stock/products/?id=" + product.id)
              .then(function (response) {
                  $scope.etablissements = response.data;
              });
      }
    };
  }]);

app.controller('ExportCtrl', ['$scope', '$http', 'DTOptionsBuilder', function($scope, $http, DTOptionsBuilder) {$scope.dtOptions = DTOptionsBuilder.newOptions().withPaginationType('full_numbers').withButtons([ 'copy', 'csv', 'excel', 'pdf', 'print']).withDOM("<'row'<'col-sm-3'l><'col-sm-4'i><'col-sm-5'f>>" + "<'row'<'col-sm-12'tr>>" + "<'row'<'col-sm-4'B><'col-sm-8'p>>").withDisplayLength(10);
  }]);



