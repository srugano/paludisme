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
var chart2;

var align_data1 = function(data){
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

var align_data2 = function(data){
  var ingredients = Object.create(null);

  data.forEach(function (a) {
    ingredients[a.dosage] = (ingredients[a.dosage] || 0) + a.quantity;
  });
  var all_data = Object.keys(ingredients).map(function (key) {  
      return { name: key, data: [ ingredients[key]]};
    });
  return all_data;
};

var update_rates = function (data){
  var rates = {nombre: 0, expected: 0};
  data.forEach(function (a) {
    rates.nombre = (rates.nombre || 0) + a.nombre ;
    rates.expected = (rates.expected || 0) + a.expected ;
  });
  document.getElementById("nombres").innerHTML = rates.nombre;
  document.getElementById("expected").innerHTML = rates.expected;
  document.getElementById("taux").innerHTML = (rates.nombre / rates.expected * 100).toFixed(2);
};

$(document).ready(function() {

    var url1 =  "/stock/casespalus/";
    var url2 =  "/stock/stockfinal/";
    $.getJSON(url1, function(data) {
        
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
            credits: {
                enabled: false
            },
            series: align_data1(data)
          }
        );
      });

    $.getJSON(url2, function(data) {
        var new_data = align_data2(data);
        chart2 = new Highcharts.chart(
          'situation_stock', 
          {
             chart: {
                type: 'bar'
            },
            title: {
                text: 'Situation de Stock'
            },
            tooltip: {
                headerFormat: '<b>{series.name}</b><br>',
                valueSuffix: ' paquest'
            },
            plotOptions: {
                bar: {
                    dataLabels: {
                        enabled: true
                    }
                }
            },
            legend: {
                layout: 'vertical',
                align: 'right',
                verticalAlign: 'top',
                x: -40,
                y: 15           ,
                floating: true,
                borderWidth: 1,
                backgroundColor: ((Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF'),
                shadow: true
            },
            credits: {
                enabled: false
            },
            xAxis: {
                categories : ['Stock']
                // crosshair: true
            },
            rangeSelector: {
                selected: 1
            },
            yAxis: {
                title: {
                    text: 'Ce qui reste en stock'
                },
                min: 0
            }, 
            series: new_data
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
        // rates
        $http.get("/stock/rates/")
        .then(function (response) {
            if (response.data.length > 0) {
                update_rates(response.data);
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
                var series = align_data1(response.data);
                chart1.series[0].setData(series[0].data);
                chart1.series[1].setData(series[1].data);
                chart1.series[2].setData(series[2].data);
                chart1.series[3].setData(series[3].data);
            });
            $http.get("/stock/stockfinal/?report__facility__district__province=" + province.id)
              .then(function (response) {
                var series = align_data2(response.data);
                chart2.series[0].setData(series[0].data);
                chart2.series[1].setData(series[1].data);
                chart2.series[2].setData(series[2].data);
                chart2.series[3].setData(series[3].data);
                chart2.series[4].setData(series[4].data);
                chart2.series[5].setData(series[5].data);
                chart2.series[6].setData(series[6].data);
                chart2.series[7].setData(series[7].data);
                chart2.series[8].setData(series[8].data);
            });
            // rates
            $http.get("/stock/rates/?facility__district__province=" + province.id)
            .then(function (response) {
                if (response.data.length > 0) {
                    update_rates(response.data);
                  }
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
                var series = align_data1(response.data);
                chart1.series[0].setData(series[0].data);
                chart1.series[1].setData(series[1].data);
                chart1.series[2].setData(series[2].data);
                chart1.series[3].setData(series[3].data);
            });
              $http.get("/stock/stockfinal/?report__facility__district=" + district.id)
              .then(function (response) {
                var series = align_data2(response.data);
                chart2.series[0].setData(series[0].data);
                chart2.series[1].setData(series[1].data);
                chart2.series[2].setData(series[2].data);
                chart2.series[3].setData(series[3].data);
                chart2.series[4].setData(series[4].data);
                chart2.series[5].setData(series[5].data);
                chart2.series[6].setData(series[6].data);
                chart2.series[7].setData(series[7].data);
                chart2.series[8].setData(series[8].data);
            });
            // rates
            $http.get("/stock/rates/?facility__district=" + district.id)
            .then(function (response) {
                if (response.data.length > 0) {
                    update_rates(response.data);
                  }
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
                var series = align_data1(response.data);
                chart1.series[0].setData(series[0].data);
                chart1.series[1].setData(series[1].data);
                chart1.series[2].setData(series[2].data);
                chart1.series[3].setData(series[3].data);
            });
              $http.get("/stock/stockfinal/?report__facility=" + cds.id)
              .then(function (response) {
                var series = align_data2(response.data);
                chart2.series[0].setData(series[0].data, false);
                chart2.series[1].setData(series[1].data, false);
                chart2.series[2].setData(series[2].data, false);
                chart2.series[3].setData(series[3].data, false);
                chart2.series[4].setData(series[4].data, false);
                chart2.series[5].setData(series[5].data, false);
                chart2.series[6].setData(series[6].data, false);
                chart2.series[7].setData(series[7].data, false);
                chart2.series[8].setData(series[8].data, false);
            });
            // rates
            $http.get("/stock/rates/?facility=" + cds.id)
            .then(function (response) {
                if (response.data.length > 0) {
                    update_rates(response.data);
                  }
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
