(function($) {
    "use strict";
})(jQuery);

var padding = { top: 20, right: 40, bottom: 0, left: 0 },
    w = 500 - padding.left - padding.right,
    h = 500 - padding.top - padding.bottom,
    r = Math.min(w, h) / 2,
    rotation = 0,
    oldrotation = 0,
    picked = 100000,
    oldpick = [],
    color = d3.scaleOrdinal(d3.schemeCategory20); // Updated for D3 v7

var data = [
    { "label": "Dell LAPTOP", "value": 1, "question": "What CSS property is used for specifying the area between the content and its border?" }, // padding
    { "label": "IMAC PRO", "value": 2, "question": "What CSS property is used for changing the font?" }, // font-family
    { "label": "SUZUKI", "value": 3, "question": "What CSS property is used for changing the color of text?" }, // color
    { "label": "HONDA", "value": 4, "question": "What CSS property is used for changing the boldness of text?" }, // font-weight
    { "label": "FERRARI", "value": 5, "question": "What CSS property is used for changing the size of text?" }, // font-size
    { "label": "APARTMENT", "value": 6, "question": "What CSS property is used for changing the background color of a box?" }, // background-color
    { "label": "IPAD PRO", "value": 7, "question": "Which word is used for specifying an HTML tag that is inside another tag?" }, // nesting
    { "label": "LAND", "value": 8, "question": "Which side of the box is the third number in: margin:1px 1px 1px 1px; ?" }, // bottom
    { "label": "MOTOROLLA", "value": 9, "question": "What are the fonts that don't have serifs at the ends of letters called?" }, // sans-serif
    { "label": "BMW", "value": 10, "question": "With CSS selectors, what character prefix should one use to specify a class?" }
];

var svg = d3.select('#chart')
    .append("svg")
    .attr("width", w + padding.left + padding.right)
    .attr("height", h + padding.top + padding.bottom);

var container = svg.append("g")
    .attr("class", "chartholder")
    .attr("transform", "translate(" + (w / 2 + padding.left) + "," + (h / 2 + padding.top) + ")");

var vis = container.append("g");

var pie = d3.pie().sort(null).value(function(d) { return 1; });
var arc = d3.arc().outerRadius(r);

var arcs = vis.selectAll("g.slice")
    .data(pie(data))
    .enter()
    .append("g")
    .attr("class", "slice");

arcs.append("path")
    .attr("fill", function(d, i) { return color(i); })
    .attr("d", function(d) { return arc(d); });

arcs.append("text")
    .attr("transform", function(d) {
        d.innerRadius = 0;
        d.outerRadius = r;
        d.angle = (d.startAngle + d.endAngle) / 2;
        return "rotate(" + (d.angle * 180 / Math.PI - 90) + ")translate(" + (d.outerRadius - 10) + ")";
    })
    .attr("text-anchor", "end")
    .text(function(d, i) {
        return data[i].label;
    });

container.on("click", spin);

function spin(d) {
    container.on("click", null);

    if (oldpick.length == data.length) {
        container.on("click", null);
        return;
    }

    var ps = 360 / data.length,
        pieslice = Math.round(1440 / data.length),
        rng = Math.floor((Math.random() * 1440) + 360);

    rotation = (Math.round(rng / ps) * ps);
    picked = Math.round(data.length - (rotation % 360) / ps);
    picked = picked >= data.length ? (picked % data.length) : picked;

    if (oldpick.indexOf(picked) !== -1) {
        d3.select(this).call(spin);
        return;
    } else {
        oldpick.push(picked);
    }

    rotation += 90 - Math.round(ps / 2);
    vis.transition()
        .duration(3000)
        .attrTween("transform", rotTween)
        .each("end", function() {
            d3.select(".slice:nth-child(" + (picked + 1) + ") path")
                .attr("fill", "#111");
            d3.select("#question h1")
                .text(data[picked].question);
            oldrotation = rotation;
            container.on("click", spin);
        });
}

svg.append("g")
    .attr("transform", "translate(" + (w + padding.left + padding.right) + "," + ((h / 2) + padding.top) + ")")
    .append("path")
    .attr("d", "M-" + (r * .15) + ",0L0," + (r * .05) + "L0,-" + (r * .05) + "Z")
    .style("fill", "black");

container.append("circle")
    .attr("cx", 0)
    .attr("cy", 0)
    .attr("r", 60)
    .style("fill", "white")
    .style("cursor", "pointer");

container.append("text")
    .attr("x", 0)
    .attr("y", 15)
    .attr("text-anchor", "middle")
    .text("SPIN")
    .style("font-weight", "bold")
    .style("font-size", "30px");

function rotTween(to) {
    var i = d3.interpolate(oldrotation % 360, rotation);
    return function(t) {
        return "rotate(" + i(t) + ")";
    };
}

function getRandomNumbers() {
    var array = new Uint16Array(1000);
    var scale = d3.scaleLinear().range([360, 1440]).domain([0, 100000]);

    if (window.hasOwnProperty("crypto") && typeof window.crypto.getRandomValues === "function") {
        window.crypto.getRandomValues(array);
    } else {
        for (var i = 0; i < 1000; i++) {
            array[i] = Math.floor(Math.random() * 100000) + 1;
        }
    }
    return array;
}

window.onload = function() {
    const progressBarFill = document.getElementById('progress-bar-fill');
    progressBarFill.style.width = '100%';

    setTimeout(function() {
        window.location.href = "/next-page";  // Replace with the URL of the next page
    }, 7000);  // 7 seconds
};
