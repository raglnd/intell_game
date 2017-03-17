var Graph = (function () {
  function findEdge(t1, id1, t2, id2, idlookup) {
      var table1 = idlookup[idlookup.indexOf(t1)+1];
      var table2 = idlookup[idlookup.indexOf(t2)+1];
      var node1;
      var node2;
  
      for (i = 0; i < table1.length; i++) {
          if (table1[i][0] == id1) {
              node1 = table1[i][1];
              break;
          }
      }
      for (i = 0; i < table2.length; i++) {
          if (table2[i][0] == id2) {
              node2 = table2[i][1];
              break;
          }
      }
      return [node1, node2];
  }
  
  function getData(tables, schema, arr, cutoff) {
      var nodesarray = [];
      var edgesarray = [];
      var idlookup = [];
      var table;
      var scheme;
      var idcount = 0;
      var tabids;
  
      //Generate Nodes
      for (i = 0; i < cutoff; i++) {
          //make node associative arrays
          table = tables[i];
          scheme = schema[table];
          tabids = [];
          for (j = 0; j < arr[i].length; j++) {
              tabids.push([arr[i][j][scheme[0]], idcount]);
              var nodelabel = "";
              var node;
              for (k = 0; k < scheme.length; k++) {
                  nodelabel += scheme[k]+" "+arr[i][j][scheme[k]]+" ";
              }
              node = {id: idcount, label: nodelabel, group: table};
              idcount++;
              nodesarray.push(node);
          }
          idlookup.push(table.toLowerCase()+"_"+scheme[0], tabids);
      }
      var nodes = new vis.DataSet(nodesarray);
      
      //Generate Edges
      var i;
      var edgesarray = []
      for (i = cutoff; i < arr.length; i++) {
          table = tables[i];
          scheme = schema[table];
          for (j = 0; j < arr[i].length; j++) {
              var f;
              var t;
              var map;
              f = arr[i][j][scheme[1]];
              t = arr[i][j][scheme[2]];
              map = findEdge(scheme[1], f, scheme[2], t, idlookup);
              edgesarray.push({from: map[0], to: map[1]});
          }
      }
      var edges = new vis.DataSet(edgesarray);
  
      var container = document.getElementById("dumpLoc");
      var data = {
          nodes: nodes,
          edges: edges
      };
      var options = {
          nodes: {
              shape: 'dot',
              size: 40
          },
          physics: {
              enabled: true,
              barnesHut: {
                  gravitationalConstant: -12000,
                  avoidOverlap: .05,
                  centralGravity: .5
              },
              maxVelocity: 20,
              minVelocity: .75
          }
      };
  
      var network = new vis.Network(container, data, options);
  }
  return {
    getData: function (table, schema, dump, split) { getData(table, schema, dump,split); },
  }
})();
