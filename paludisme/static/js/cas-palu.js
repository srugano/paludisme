var app = angular.module('PaludismeApp', ['ngSanitize', 'datatables', 'datatables.buttons']);

app.service('sharedProperties', function () {

    var hashtable = {};
    var _provinceObj = {};
    this.provinceObj = _provinceObj;

    return {
        setValue: function (key, value) {
            hashtable[key] = value;
        },
        getValue: function (key) {
            return hashtable[key];
        }
    };
});

var shared_province;
var shared_district;
var shared_cds;

app.controller('FilterCtrl', ['$scope', '$http', 'sharedProperties', function($scope, $http, sharedProperties) {

        // province
        $http.get("/bdiadmin/province/")
        .then(function (response) {
            if (response.data.length > 0) {
                $scope.provinces = response.data;
            }
        });

        $scope.update_province = function () {
            var province = $scope.province;
            if (province) {
              $http.get("/bdiadmin/district/?province=" + province.id)
              .then(function (response) {
                $scope.districts = response.data;
                shared_province = province;
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
                  shared_district = district;
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
                  shared_cds = cds;
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

var align_data = function(data){
  var ingredients = Object.create(null);
  var simples= 0;
  var accutes= 0;
  var pregnant_womens= 0;
  var deceases= 0;
  var ges= 0;
  var tdrs= 0;

  data.forEach(function (a) {
    ingredients[a.province] = [(ingredients[a.province] || 0) + a.simple];
    console.log(ingredients);
  });
  var all_data = Object.keys(ingredients).map(function (key) {  
      return { province: key, data: [ ingredients[key]]};
    });
  return all_data;
};


app.controller('ExportCtrl', ['$scope', '$http', 'DTOptionsBuilder', 'sharedProperties', function($scope, $http, DTOptionsBuilder, sharedProperties) {
    // for export
    $scope.dtOptions = DTOptionsBuilder.newOptions().withPaginationType('full_numbers').withButtons([ 'copy', 'csv', 'excel', 'pdf', 'print']).withDOM("<'row'<'col-sm-3'l><'col-sm-4'i><'col-sm-5'f>>" + "<'row'<'col-sm-12'tr>>" + "<'row'<'col-sm-4'B><'col-sm-8'p>>").withDisplayLength(10);
      // province
      $http.get("/stock/casespalus2/")
      .then(function (response) {
          if (response.data.length > 0) {
          $scope.provincesss = response.data;
              // console.log(align_data(response.data));
          }
      });
    // two way binding
  }]);
