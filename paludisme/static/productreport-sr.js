var app = angular.module('RepportApp', [ 'datatables', 'datatables.buttons']);

app.controller('RepportCtrl', ['$scope', '$http', 'DTOptionsBuilder', function($scope, $http, DTOptionsBuilder) {
    // for datatable 
      $scope.dtOptions = DTOptionsBuilder.newOptions().withPaginationType('full_numbers').withButtons([ 'copy', 'csv', 'excel', 'pdf', 'print']).withDOM("<'row'<'col-sm-3'l><'col-sm-4'i><'col-sm-5'f>>" + "<'row'<'col-sm-12'tr>>" + "<'row'<'col-sm-4'B><'col-sm-8'p>>").withDisplayLength(10);
      
        $http.get("/stock/productreports/?category=SR")
        .then(function (response) {
          $scope.reports = response.data;
      });
}]);