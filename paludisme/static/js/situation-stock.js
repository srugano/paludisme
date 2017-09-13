var app = angular.module('PaludismeApp', ['ngSanitize', 'datatables', 'datatables.buttons', "ui.bootstrap.modal"]);

app.controller('FilterCtrl', ['$scope', '$http', 'DTOptionsBuilder', function($scope, $http, DTOptionsBuilder) {

        // province
        $http.get("/bdiadmin/province/")
        .then(function (response) {
            if (response.data.length > 0) {
                $scope.provinces = response.data;
            } 
        });
        $http.get("/stock/stockfinalprov/")
        .then(function (response) {
            if (response.data.length > 0) {
            $scope.structures = response.data;
            }
        });
        // product
        $http.get("/stock/products/")
        .then(function (response) {
            if (response.data.length > 0) {
            $scope.products = response.data;
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
            $http.get("/stock/stockfinalprov/?province=" + province.id)
              .then(function (response) {
                  $scope.districtss = false;
                  $scope.cdsss = false;
                  if (response.data.length > 0) {
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
              $http.get("/stock/stockfinaldis/?district=" + district.id)
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
              $http.get("/bdiadmin/cds/" + cds.id + "/" )
              .then(function (response) {
                  $scope.etablissements = response.data;
              });
              $http.get("/stock/stockfinalcds/?cds=" + cds.id)
              .then(function (response) {
                  if (response.data.length > 0) {
                  $scope.structures = response.data;
                  } else  $scope.structures = {};
              });
      }
    };
    // Export
    $scope.dtOptions = DTOptionsBuilder.newOptions().withPaginationType('full_numbers').withButtons([ 'copy', 'csv', 'excel', 'pdf', 'print']).withDOM("<'row'<'col-sm-3'l><'col-sm-4'i><'col-sm-5'f>>" + "<'row'<'col-sm-12'tr>>" + "<'row'<'col-sm-4'B><'col-sm-8'p>>").withDisplayLength(25);

    // modal export
    $scope.open = function() {
        $scope.reports = {};
        if($(this)[0].y.cds){
          $http.get("/stock/reportsST/?facility=" + $(this)[0].y.id +"&week=" + $(this)[0].y.week).then(function (response) {
                if (response.data.length > 0) {
                  $scope.reports = response.data;
                    }
            });
        } else if ($(this)[0].y.district){
          $http.get("/stock/reportsST/?facility__district=" + $(this)[0].y.id +"&week=" + $(this)[0].y.week).then(function (response) {
                if (response.data.length > 0) {
                  $scope.reports = response.data;
                    }
            });
        } else if ($(this)[0].y.province) {
          $http.get("/stock/reportsST/?facility__district__province=" + $(this)[0].y.id +"&week=" + $(this)[0].y.week).then(function (response) {
                if (response.data.length > 0) {
                  $scope.reports = response.data;
                    }
            });
        }
        $scope.showModal = true;
      };

      $scope.ok = function() {
      $scope.showModal = false;
    };
}]);


app.controller('ExportCtrl', ['$scope', '$http', 'DTOptionsBuilder', function($scope, $http, DTOptionsBuilder) {$scope.dtOptions = DTOptionsBuilder.newOptions().withPaginationType('full_numbers').withButtons([ 'copy', 'csv', 'excel', 'pdf', 'print']).withDOM("<'row'<'col-sm-3'l><'col-sm-4'i><'col-sm-5'f>>" + "<'row'<'col-sm-12'tr>>" + "<'row'<'col-sm-4'B><'col-sm-8'p>>").withDisplayLength(25);}]);