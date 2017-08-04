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