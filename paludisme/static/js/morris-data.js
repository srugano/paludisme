$(function() {

    Morris.Donut({
        element: 'morris-donut-chart',
        data: [{
            label: "Rapports attendus",
            value: 72
        }, {
            label: "Rapports recus",
            value: 71
        }, {
            label: "Taux de raportage",
            value: 99
        }],
        resize: true
    });
    
});
