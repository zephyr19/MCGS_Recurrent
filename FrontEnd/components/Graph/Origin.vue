<template>
  <div class="wrapper origin" v-loading="originLoading">
    <div class="origin-header">
      <span class="origin-title">original graph</span>
      <span class="origin-info" v-show="graphRecord.edge_num"
        ><b>Edges:</b>{{ graphRecord.edge_num }} <b>Nodes:</b
        >{{ graphRecord.node_num }}</span
      >
    </div>
    <span class="origin-tip" v-show="dataset === ''"
      >please select graph data set</span
    >

    <!-- <div
      role="tooltip"
      id="no_tip"
      aria-hidden="false"
      class="el-popover el-popper el-popover--plain my-no-tip"
      tabindex="0"
      x-placement="bottom"
    >
      there are no <b>{{ select_minotype }}s</b> in this graph
    </div> -->
  </div>
</template>

<script>
import { mapState } from 'vuex'
import * as d3 from 'd3'
import fisheye from '../../utils/fisheye'

export default {
  data() {
    return {}
  },
  computed: {
    ...mapState(['dataset', 'originLoading', 'graphRecord']),
    originFisheyeFile() {
      return `json_files/origin_${this.dataset.toLowerCase()}.json`
    },
    samplingFisheyeFile() {
      return 'json_files/sampling_result.json'
    },
  },
  watch: {
    originLoading(newValue, oldValue) {
      let self = this
      if (newValue) {
        d3.json(self.originFisheyeFile).then(function (data) {
          d3.select('.origin').selectAll('svg').remove()
          let svg = d3
            .select('.origin')
            .append('svg')
            .attr('width', data.svg_width)
            .attr('height', data.svg_height)
            .attr('viewBox', data.svg_viewBox)

          let g = svg.append('g')

          let links = g
            .selectAll('.link')
            .data(data.links)
            .enter()
            .append('line')
            .attr('class', 'link')
            .attr('x1', (d) => {
              return data.nodes[d.source].cx
            })
            .attr('y1', (d) => {
              return data.nodes[d.source].cy
            })
            .attr('x2', (d) => {
              return data.nodes[d.target].cx
            })
            .attr('y2', (d) => {
              return data.nodes[d.target].cy
            })
            .style('stroke', '#bcbcbc')

          let nodes = g
            .selectAll('.node')
            .data(data.nodes)
            .enter()
            .append('circle')
            .attr('id', (d) => {
              return d.id
            })
            .attr('cx', (d) => {
              return d.cx
            })
            .attr('cy', (d) => {
              return d.cy
            })
            .attr('r', (d) => {
              return d.r
            })
            .style('fill', '#ccc')
            .style('stroke', '#666')

          let parentNode = document.querySelector('.origin')
          parentNode.setAttribute('fisheye', true)
          let parentWidth = parentNode.clientWidth
          let parentHeight = parentNode.clientHeight
          let svgWidth = svg.attr('width').replace('px', '')
          let svgHeight = svg.attr('height').replace('px', '')
          let margin = { left: 20, right: 20, top: 20, bottom: 20 }
          let scaleNum = d3.min([
            (parentWidth - margin.left - margin.right) / svgWidth,
            (parentHeight - margin.top - margin.bottom) / svgHeight,
          ])
          svgWidth *= scaleNum
          svgHeight *= scaleNum
          svg.attr('width', svgWidth).attr('height', svgHeight)
          // .style('transform', 'translate(')

          // add zoom functionality
          let zoomer = d3
            .zoom()
            .scaleExtent([1, 100])
            .on('zoom', (event) => {
              let scale = event.transform.k
              if (scale === 1) {
                parentNode.setAttribute('fisheye', true)
              } else {
                parentNode.setAttribute('fisheye', false)
              }
              g.attr('transform', event.transform)
            })
          svg.call(zoomer)

          // add fisheye functionality
          g.on('mousemove', (event) => {
            if (parentNode.getAttribute('fisheye') === 'true') {
              let eye = fisheye.circular().radius(svgWidth / 5)
              eye.focus(d3.pointer(event))
              nodes
                .each((d) => {
                  d.fisheye = eye(d)
                })
                .attr('cx', (d) => {
                  return d.fisheye.x
                })
                .attr('cy', (d) => {
                  return d.fisheye.y
                })
                .attr('r', (d) => {
                  return d.fisheye.z * d.r
                })

              links
                .attr('x1', (d) => {
                  return data.nodes[d.source].fisheye.x
                })
                .attr('y1', (d) => {
                  return data.nodes[d.source].fisheye.y
                })
                .attr('x2', (d) => {
                  return data.nodes[d.target].fisheye.x
                })
                .attr('y2', (d) => {
                  return data.nodes[d.target].fisheye.y
                })
            }
          })

          self.$store.commit('SET_ORIGINLOADING', false)
        })
      }
    },
  },
}
</script>

<style lang="scss">
.origin {
  color: #999;
}

.origin-header {
  display: flex;
  justify-content: space-between;
}

.origin-tip {
  // position: absolute;
  // top: 50%;
  // left: 50%;
  // transform: translate(-50%, -50%);
}
</style>
