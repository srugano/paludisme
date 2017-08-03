'use strict';


// Copy & Paste this
Date.prototype.getUnixTime = function() { return this.getTime()/1000|0 };
if(!Date.now) Date.now = function() { return new Date(); }
Date.time = function() { return Date.now().getUnixTime(); }

function getDateOfWeek(w, y) {
    var d = (1 + (w - 1) * 7); // 1st of January + 7 days for each week
    return new Date(y, 0, d).getUnixTime();
}


Highcharts.setOptions({
    global: {
        /**
         * Use moment-timezone.js to return the timezone offset for individual
         * timestamps, used in the X axis labels and the tooltip header.
         */
        getTimezoneOffset: function (timestamp) {
            var zone = 'Africa/Bujumbura',
                timezoneOffset = -moment.tz(timestamp, zone).utcOffset();

            return timezoneOffset;
        }
    }
});

var chart1;

var align_data = function(data){
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
      simples.push([getDateOfWeek(item.week,item.year),simple]);
      lookup[acute] = 1;
      acutes.push([getDateOfWeek(item.week,item.year), acute]);
      lookup[pregnant_women] = 1;
      pregnant_womens.push([getDateOfWeek(item.week,item.year),pregnant_women]);
      lookup[decease] = 1;
      deceases.push([getDateOfWeek(item.week,item.year),decease]);
    }
  }
  return [{name: 'Simple', data:simples}, {name: 'Acute', data: acutes }, {name:"Pregnant women", data: pregnant_womens}, {name: "Decease", data:deceases}];
};

$(document).ready(function() {

    var url =  "/stock/casespalus/?";
    $.getJSON(url, function(data) {
        
        chart1 = new Highcharts.chart(
          'situation_cas_palu', 
          {
             chart: {
                type: 'spline',
                 zoomType: 'x'
            },
            title: {
                text: 'Nombres de cas de paludisme'
            },
            tooltip: {
                headerFormat: '<b>{series.name}</b><br>',
                pointFormat: '{point.x:%e. %b}: {point.y:.0f} cas'
            },
            xAxis:
              { 
                type: 'datetime',
                title: {
                    text: 'Date'
                },
              },
            rangeSelector: {
                selected: 1
            },
            yAxis: {
                title: {
                    text: 'Cas de paludisme'
                },
                min: 0
            }, 
            series: align_data(data)
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
        $scope.update_province = function () {
            var province = $scope.province;
            if (province) {
              $http.get("/bdiadmin/district/?province=" + province.id)
              .then(function (response) {
                $scope.districts = response.data;
            });
            $http.get("/stock/casespalus/?report__facility__district__province=" + province.id)
              .then(function (response) {
                var series = align_data(response.data);
                chart1.series[0].setData(series[0].data);
                chart1.series[1].setData(series[1].data);
                chart1.series[2].setData(series[2].data);
                chart1.series[3].setData(series[3].data);
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
              $http.get("/stock/casespalus/?report__facility__district=" + district.id)
              .then(function (response) {
                var series = align_data(response.data);
                chart1.series[0].setData(series[0].data);
                chart1.series[1].setData(series[1].data);
                chart1.series[2].setData(series[2].data);
                chart1.series[3].setData(series[3].data);
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
              $http.get("/stock/casespalus/?report__facility=" + cds.id)
              .then(function (response) {
                var series = align_data(response.data);
                chart1.series[0].setData(series[0].data);
                chart1.series[1].setData(series[1].data);
                chart1.series[2].setData(series[2].data);
                chart1.series[3].setData(series[3].data);
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



