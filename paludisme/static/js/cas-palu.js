var app = angular.module('PaludismeApp', ['ngSanitize', 'datatables', 'datatables.buttons', "ui.bootstrap.modal"]);



app.controller('FilterCtrl', ['$scope', '$http', '$locale', 'DTOptionsBuilder', function($scope, $http, $locale, DTOptionsBuilder) {
        $locale.NUMBER_FORMATS.GROUP_SEP = ' ';
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
              $http.get("/stock/casespalusProv/?id=" + province.id + "&startdate=" + $scope.startdate + "&enddate=" + $scope.enddate)
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
              $http.get("/stock/casespalusDis/?id=" + district.id + "&startdate=" + $scope.startdate + "&enddate=" + $scope.enddate)
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
              $http.get("/stock/casespalusCds/?id=" + cds.id + "&startdate=" + $scope.startdate + "&enddate=" + $scope.enddate)
              .then(function (response) {
                  if (response.data.length > 0) {
                  $scope.structures = response.data;
                  } else  $scope.structures = {};
              });
      }
    };
    // for export
    $scope.dtOptions = DTOptionsBuilder.newOptions().withPaginationType('full_numbers').withButtons([ 'copy', 'csv', 'excel', 'pdf', 'print']).withDOM("<'row'<'col-sm-3'l><'col-sm-4'i><'col-sm-5'f>>" + "<'row'<'col-sm-12'tr>>" + "<'row'<'col-sm-4'B><'col-sm-8'p>>").withDisplayLength(25);  

    $scope.open = function() {
      $scope.reports = {};
      if($(this)[0].y.cds){
        $http.get("/stock/reportsCA/?facility=" + $(this)[0].y.id + "&startdate=" + $scope.startdate + "&enddate=" + $scope.enddate).then(function (response) {
              if (response.data.length > 0) {
                $scope.reports = response.data;
                  }
          });
      } else if ($(this)[0].y.district){
        $http.get("/stock/reportsCA/?facility__district=" + $(this)[0].y.id + "&startdate=" + $scope.startdate + "&enddate=" + $scope.enddate).then(function (response) {
              if (response.data.length > 0) {
                $scope.reports = response.data;
                  }
          });
      } else if ($(this)[0].y.province) {
        $http.get("/stock/reportsCA/?facility__district__province=" + $(this)[0].y.id + "&startdate=" + $scope.startdate + "&enddate=" + $scope.enddate).then(function (response) {
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
        $http.get("/stock/casespalusCds/?id=" + cds.id + "&startdate=" + startdate + "&enddate=" + enddate).then(function (response) {
              if (response.data.length > 0) {
                $scope.structures = response.data;
                  }
          });
      } else if (district){
        $http.get("/stock/casespalusDis/?id=" + district.id + "&startdate=" + startdate + "&enddate=" + enddate).then(function (response) {
              if (response.data.length > 0) {
                $scope.structures = response.data;
                  }
          });
      } else if (province) {
        $http.get("/stock/casespalusProv/?id=" + province.id + "&startdate=" + startdate + "&enddate=" + enddate).then(function (response) {
              if (response.data.length > 0) {
                $scope.structures = response.data;
                  }
          });
      } else {
        $http.get("/stock/casespalusProv/?startdate=" + startdate + "&enddate=" + enddate).then(function (response) {
              if (response.data.length > 0) {
                $scope.structures = response.data;
                  }
          });

      }
    };
}]);
