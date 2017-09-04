var app = angular.module('PaludismeApp', ['ngSanitize', 'datatables', 'datatables.buttons']);

app.controller('FilterCtrl', ['$scope', '$http', 'DTOptionsBuilder',  function($scope, $http, DTOptionsBuilder) {
        $scope.districtss = false;
        $scope.cdsss = false;
        // province
        $http.get("/bdiadmin/province/")
        .then(function (response) {
            if (response.data.length > 0) {
                $scope.provinces = response.data;
            }
        });
          // province
          $http.get("/stock/casespalusProv/")
          .then(function (response) {
              if (response.data.length > 0) {
              $scope.structures = response.data;
              }
          });

        $scope.update_province = function () {
            var province = $scope.province;
            if (province) {
              $http.get("/bdiadmin/district/?province=" + province.id)
                .then(function (response) {
                  $scope.districts = response.data;
                  $scope.cdss = "";
              });
              $http.get("/stock/casespalusProv/?report__facility__district__province=" + province.id)
              .then(function (response) {
                  $scope.districtss = false;
                  $scope.cdsss = false;
                  if (response.data.length > 0) {
                  console.log($scope.cdsss, $scope.districtss);
                  $scope.structures = response.data;
                  }
              });
          }
      };
          // district
          $scope.update_district = function () {
            var district = $scope.district;
            $scope.districtss = true;
            if (district) {
              $http.get("/bdiadmin/cds/?district=" + district.id)
              .then(function (response) {
                  $scope.cdss = response.data;
              });
              $http.get("/stock/casespalusDis/?report__facility__district=" + district.id)
              .then(function (response) {
                  $scope.cdsss = false;
                  if (response.data.length > 0) {
                  $scope.structures = response.data;
                  }
              });
          }
      };
        // CDS
        $scope.update_cds = function () {
            var cds = $scope.cds;
            $scope.districtss = true;
            $scope.cdsss = true;
            if (cds) {
              $http.get("/stock/casespalusCds/?report__facility=" + cds.id)
              .then(function (response) {
                  if (response.data.length > 0) {
                  $scope.structures = response.data;
                  } else  $scope.structures = {};
              });
      }
    };
    // for export
    $scope.dtOptions = DTOptionsBuilder.newOptions().withPaginationType('full_numbers').withButtons([ 'copy', 'csv', 'excel', 'pdf', 'print']).withDOM("<'row'<'col-sm-3'l><'col-sm-4'i><'col-sm-5'f>>" + "<'row'<'col-sm-12'tr>>" + "<'row'<'col-sm-4'B><'col-sm-8'p>>").withDisplayLength(10);  
  }]);

