var color = d3.scale.category20();
var links = [
  {source: 0, target: 1},
  {source: 0, target: 2},
  {source: 0, target: 3},
  {source: 4, target: 5},
  {source: 5, target: 18},
  {source: 5, target: 6},
  {source: 6, target: 1},
  {source: 4, target: 7},
  {source: 7, target: 8},
  {source: 4, target: 9},
  {source: 10, target: 11},
  {source: 11, target: 12},
  {source: 11, target: 13},
  {source: 11, target: 14},
  {source: 10, target: 15},
  {source: 15, target: 16},
  {source: 15, target: 17}
];

var nodes = [
  {"name":"Movie", "group":1, "value":15, "uri":"http://www.naver.com"},
  {"name":"Inception", "group":2, "value":10},
  {"name":"Tazza", "group":2, "value":10},
  {"name":"Birdman", "group":2, "value":10},
  {"name":"Music", "group":1, "value":15},
  {"name":"Classic", "group":3, "value":10},
  {"name":"Hans Zimmer", "group":3, "value":8},
  {"name":"Hip-hop", "group":3, "value":10},
  {"name":"Dynamic Duo", "group":3, "value":8},
  {"name":"K-pop", "group":3, "value":8},
  {"name":"HCI", "group":1, "value":15},
  {"name":"Data visualization", "group":4, "value":10},
  {"name":"Danchew", "group":4, "value":8},
  {"name":"Planit", "group":4, "value":8},
  {"name":"Sawtooth chart", "group":4, "value":8},
  {"name":"Web programming", "group":5, "value":10},
  {"name":"Portfolio", "group":5, "value":8},
  {"name":"Team blog", "group":5, "value":8},
  {"name":"Rachmaninov", "group":3, "value":8} //18
];
var width = 960, height = 500;
var force = d3.layout.force()
  .nodes(nodes)
  .links(links)
  .size([width, height])
  .linkDistance(60)
  .charge(-300)
  .on("tick", tick)
  .start();
var svg = d3.select("#graph-container").append("svg")
  .attr("width", width)
  .attr("height", height)
  .append("g");
var link = svg.selectAll(".link")
  .data(force.links())
  .enter().append("line")
  .attr("class", "link");
var node = svg.selectAll(".node")
  .data(force.nodes())
  .enter().append("g")
  .attr("class", "node")
  .attr("link", function(d) { return d.uri; })
  .on("mouseover", mouseover)
  .on("mouseout", mouseout)
  .on("click", click)
  .call(force.drag);
node.append("circle")
  .style("fill", function(d) { return color(d.group); })
  .attr("selected", 0)
  .attr("r", function(d) { return d.value; });
node.append("text")
  .attr("x", 12)
  .attr("dy", ".35em")
  .text(function(d) { return d.name; })
  .style("visibility", "hidden");
function tick() {
  link
    .attr("x1", function(d) { return d.source.x; })
    .attr("y1", function(d) { return d.source.y; })
    .attr("x2", function(d) { return d.target.x; })
    .attr("y2", function(d) { return d.target.y; });
  node
    .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });
  }
function mouseover() {
  d3.selectAll("circle").style("opacity", 0.5);
  d3.select(this).select("circle").style("opacity", 1);
  d3.select(this).select("text").style("visibility", "visible");
  }
function mouseout() {
  d3.selectAll("circle").style("opacity", 1);
  d3.select(this).select("text").style("visibility", "hidden");
  }
function click(){
  var cur_state = d3.select(this).select("circle").attr("selected");
  if(cur_state==1){
    d3.select(this).select("circle").attr("selected", 0);
    window.location.href = this.getAttribute("link");
  }
  else{
    d3.selectAll("circle").style("stroke", "white");
    d3.selectAll("circle").attr("cursor", "default");
    d3.selectAll("circle").attr("selected", 0);
    d3.select(this).select("circle").style("stroke", "black");
    d3.select(this).select("circle").attr("selected", 1);
    d3.select(this).select("circle").attr("cursor", "pointer");
  }
}
function redraw(){
  vis.attr("transform",
    "translate(" + d3.event.translate + ")"
    + " scale(" + d3.event.scale + ")");
}
