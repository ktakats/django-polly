function plotResults(data){

  var dat=data.data;
  var all=0;
  for(var x=0; x<dat.length; x++){
    all+=dat[x][1]
  }

  var canvas=d3.select(".resultplot").append("svg")
    .attr("width", 1000)
    .attr("height", 1000);

  var tip=d3.select(".resultplot").append("div");
  var color = d3.scaleOrdinal(d3.schemeCategory20);

  var group= canvas.append("g")
    .attr("transform", "translate(500,200)");

  var r=200;
  var p=Math.PI *2;

  var arc=d3.arc()
    .innerRadius(0)
    .outerRadius(r)

  var pie=d3.pie()
    .value(function(d){return d[1]/all})
    .startAngle(0)
    .endAngle(p)
    .sort(null);

  var arcs=group.selectAll(".arc")
    .data(pie(dat))
    .enter()
    .append("g")
    .attr("class", "arc")

  arcs.append("path")
    .attr("d", arc)
    .attr("fill", function(d,i){return color(i)})
    .transition()
      //.delay(function(d,i){return i*500;})
      .duration(500)
    .attrTween("d", function(d){
      var i=d3.interpolate(d.startAngle+0.1,d.endAngle);
      return function(t){
        d.endAngle=i(t);
        return arc(d);
      }
    });

  arcs.append("text")
    .attr("transform", function(d){return "translate("+arc.centroid(d) + ")";})
    .attr("text-anchor", "middle")
    .attr("font-size", "1.5em")
    .transition()
    .delay(500)
    .text(function(d){if(d.data[1]>0){
      if(d.endAngle-d.startAngle<1.57 && d.data.option.length>10){
        return d.data.option.slice(0,10)+"..."
      }
      else{
      return d.data[0];}}});

  arcs.on("mouseover", function(d){
    var p=d3.select(this);
    p.attr("class", "mouseover")
    tip.html("<span>"+ d.data[0] + "</span> </br> <span>Votes: "+ d.data[1] + "</span>")
    tip.transition()
    .attr("class", "tooltip")
    .delay(200)
    .style("opacity", 0.8)
    .style("left", d3.event.pageX + 5 +"px")
    .style("top", d3.event.pageY -25+"px")
  });

  arcs.on("mouseout", function(d){
    var p=d3.select(this)
    p.attr("class", "mouseout")
    tip.transition()
    .delay(100)
    .style("opacity", 0)
  });

};
