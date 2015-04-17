$(function() {
    console.log('>>> jQuery is ready');

    /*
     * Site Control Script
     */
    $('#search').on('click', function() {
        var formData = $('#searchForm').serializeObject();

        // TODO: Your API HERE
        $.ajax({
            type: 'POST',
            url: '/search',
            data: JSON.stringify(formData),
            contentType: 'application/json; charset=utf-8',
            dataType: 'json',
            cache: false,
            processData: false,
            async: true,
            beforeSend: function() {
                // TODO
            },
            success: function(data) {
                console.log(data);
                chart.highlight(data);
            },
        });
    });

    $('#anomies').on('click', function() {
        // TODO: Your API Here
        $.ajax({
            type: 'POST',
            url: '#',
            data: JSON.stringify(formData),
            contentType: 'application/json; charset=utf-8',
            dataType: 'json',
            cache: false,
            processData: false,
            async: true,
            beforeSend: function() {
                // TODO
            },
            success: function(data) {
                // TODO
            },
        });
    });

    $('#clear_highlight').on('click', function(){
        chart.clear_highlight();
    });
    


    $('#dataSource').on('change', function() {
        // TODO: Your API Here
        $.ajax({
            type: 'GET',
            url: '/get_ts',
            dataType: 'json',
            cache: false,
            processData: false,
            async: true,
            beforeSend: function() {
                // TODO
            },
            success: function(data) {
                console.log("Initializing chart");
                chart.init(data);
            },
        });
    });
});
    /*
     * Chart Render Script
     */

    
var chart = {
    xScale: null,
    yScale: null,

    // Initial chart
    init: function (data) {
        var vis = d3.select("#visualisation"),
            WIDTH = 1400,
            HEIGHT = 500,
            MARGINS = {
                top: 20,
                right: 20,
                bottom: 20,
                left: 50
            };

        chart.xScale = d3.scale.linear().range([MARGINS.left, WIDTH - MARGINS.right]).domain([d3.min(data, function(d) { return d.x;}), 
                    d3.max(data, function(d) { return d.x;})]);

        chart.yScale = d3.scale.linear().range([HEIGHT - MARGINS.top, MARGINS.bottom]).domain([d3.min(data, function(d) { return d.y;}), 
                    d3.max(data, function(d) { return d.y;})]);

        var xAxis = d3.svg.axis()
                .scale(chart.xScale),

                yAxis = d3.svg.axis()
                .scale(chart.yScale)
                .orient("left");

        vis.append("svg:g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + (HEIGHT - MARGINS.bottom) + ")")
            .call(xAxis);

        vis.append("svg:g")
            .attr("class", "y axis")
            .attr("transform", "translate(" + (MARGINS.left) + ",0)")
            .call(yAxis);

        var lineGen = d3.svg.line()
            .x(function(d) {
                return chart.xScale(d.x);
            })
            .y(function(d) {
                return chart.yScale(d.y);
            });

        vis.append('svg:path')
            .attr('d', lineGen(data))
            .attr('stroke', 'green')
            .attr('stroke-width', 2)
            .attr('fill', 'none');
    }
    ,
    highlight: function (data) {
        var vis = d3.select("#visualisation");
        vis.selectAll("rect")
            .data(data)
            .enter()
            .append("rect")
            .attr("x", function(d) {return chart.xScale(d.start);})
            .attr("y", 20) //hardcoded, need to parameterize later
            .attr("height", 470) //hardcoded, need to parameterize later
            .attr("width", function(d) {return chart.xScale(d.stop) - chart.xScale(d.start);})
            .attr("fill", "teal")
            .attr("fill-opacity", 0.3);
    }
    ,
    clear_highlight: function (data) {
        var vis = d3.select("#visualisation");
        vis.selectAll("rect").remove();
    }
};




/* 
 * Helping functions
 */

$.fn.serializeObject = function() {
    var o = {};
    var a = this.serializeArray();
    $.each(a, function() {
        if (o[this.name]) {
            if (!o[this.name].push) {
                o[this.name] = [o[this.name]];
            }
            o[this.name].push(this.value || '');
        } else {
            if (this.name.indexOf("[]") > -1) { //if it is array
                o[this.name] = [this.value || ''];
            } else {
                o[this.name] = this.value || '';
            }
        }
    });
    return o;
};