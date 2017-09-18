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
            $http.get("/stock/stockfinalprov/?id=" + province.id + "&startdate=" + $scope.startdate + "&enddate=" + $scope.enddate + "&product=" + $scope.product.id)
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
              $http.get("/stock/stockfinaldis/?id=" + district.id + "&startdate=" + $scope.startdate + "&enddate=" + $scope.enddate + "&product=" + $scope.product.id)
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
              $http.get("/stock/stockfinalcds/?id=" + cds.id + "&startdate=" + $scope.startdate + "&enddate=" + $scope.enddate + "&product=" + $scope.product.id)
              .then(function (response) {
                  if (response.data.length > 0) {
                  $scope.structures = response.data;
                  } else  $scope.structures = {};
              });
      }
    };

    // CDS
        $scope.update_product = function () {
            var product = $scope.product;
            if (product) {
              var province = $scope.province;
              var district = $scope.district;
              var cds = $scope.cds;
              var enddate = $scope.enddate;
              var startdate = $scope.startdate;
              $scope.reports = {};
              if(cds){
                $http.get("/stock/stockfinalcds/?id=" + cds.id + "&startdate=" + startdate + "&enddate=" + enddate + "&product=" + $scope.product.id).then(function (response) {
                      if (response.data.length > 0) {
                        $scope.structures = response.data;
                          }
                  });
              } else if (district){
                $http.get("/stock/stockfinaldis/?id=" + district.id + "&startdate=" + startdate + "&enddate=" + enddate + "&product=" + $scope.product.id).then(function (response) {
                      if (response.data.length > 0) {
                        $scope.structures = response.data;
                          }
                  });
              } else if (province) {
                $http.get("/stock/stockfinalprov/?id=" + province.id + "&startdate=" + startdate + "&enddate=" + enddate + "&product=" + $scope.product.id).then(function (response) {
                      if (response.data.length > 0) {
                        $scope.structures = response.data;
                          }
                  });
              } else {
                $http.get("/stock/stockfinalprov/?startdate=" + startdate + "&enddate=" + enddate + "&product=" + $scope.product.id).then(function (response) {
                      if (response.data.length > 0) {
                        $scope.structures = response.data;
                          }
                  });
                }
              }
            };

    // Export
    $scope.dtOptions = DTOptionsBuilder.newOptions().withPaginationType('full_numbers').withButtons([ 'copy', 'csv', 'excel', 'pdf', 'print']).withDOM("<'row'<'col-sm-3'l><'col-sm-4'i><'col-sm-5'f>>" + "<'row'<'col-sm-12'tr>>" + "<'row'<'col-sm-4'B><'col-sm-8'p>>").withDisplayLength(25);

    // modal export
    $scope.open = function() {
        $scope.reports = {};
        if($(this)[0].y.cds){
          $http.get("/stock/reportsST/?facility=" + $(this)[0].y.id + "&startdate=" + $scope.startdate + "&enddate=" + $scope.enddate).then(function (response) {
                if (response.data.length > 0) {
                  $scope.reports = response.data;
                    }
            });
        } else if ($(this)[0].y.district){
          $http.get("/stock/reportsST/?facility__district=" + $(this)[0].y.id + "&startdate=" + $scope.startdate + "&enddate=" + $scope.enddate).then(function (response) {
                if (response.data.length > 0) {
                  $scope.reports = response.data;
                    }
            });
        } else if ($(this)[0].y.province) {
          $http.get("/stock/reportsST/?facility__district__province=" + $(this)[0].y.id + "&startdate=" + $scope.startdate + "&enddate=" + $scope.enddate).then(function (response) {
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

    // startdate
    $scope.get_by_date = function () {
      var province = $scope.province;
      var district = $scope.district;
      var cds = $scope.cds;
      var enddate = $scope.enddate;
      var startdate = $scope.startdate;
      $scope.reports = {};
      if(cds){
        $http.get("/stock/stockfinalcds/?id=" + cds.id + "&startdate=" + startdate + "&enddate=" + enddate + "&product=" + $scope.product.id).then(function (response) {
              if (response.data.length > 0) {
                $scope.structures = response.data;
                  }
          });
      } else if (district){
        $http.get("/stock/stockfinaldis/?id=" + district.id + "&startdate=" + startdate + "&enddate=" + enddate + "&product=" + $scope.product.id).then(function (response) {
              if (response.data.length > 0) {
                $scope.structures = response.data;
                  }
          });
      } else if (province) {
        $http.get("/stock/stockfinalprov/?id=" + province.id + "&startdate=" + startdate + "&enddate=" + enddate + "&product=" + $scope.product.id).then(function (response) {
              if (response.data.length > 0) {
                $scope.structures = response.data;
                  }
          });
      } else {
        $http.get("/stock/stockfinalprov/?startdate=" + startdate + "&enddate=" + enddate + "&product=" + $scope.product.id).then(function (response) {
              if (response.data.length > 0) {
                $scope.structures = response.data;
                  }
          });

      }
    };
}]);


app.controller('ExportCtrl', ['$scope', '$http', 'DTOptionsBuilder', function($scope, $http, DTOptionsBuilder) {$scope.dtOptions = DTOptionsBuilder.newOptions().withPaginationType('full_numbers').withButtons([ 'copy', 'csv', 'excel', 'pdf', 'print']).withDOM("<'row'<'col-sm-3'l><'col-sm-4'i><'col-sm-5'f>>" + "<'row'<'col-sm-12'tr>>" + "<'row'<'col-sm-4'B><'col-sm-8'p>>").withDisplayLength(25);}]);