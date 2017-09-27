<template>
<form class="sidebar">
    <div class="widget widget-search animated zoomInLeft">
      <input class="search-input" placeholder="Enter an ECLI number.."></input>
    </div>
  <div class="widget widget-main">
    <div class="widget-section">
        <h3>Document details</h3>
    </div>
  </div>
  </form>
</template>

<script>
import Graph from './Graph.vue'
export default {
  data () {
    return {
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>

.sidebar {
    display: flex;
    flex-direction: column;
    margin: 28px;
    width: 360px;
    position: absolute;
}

.widget {
    display: flex;
    flex-direction: column;
    padding: 8px;
    background-color: #fdfdfd;
    width: 360px;
    border-radius: 7px;
    box-shadow: 2px 2px 12px rgba(0, 0, 0, 0.22);
    color: #777;
}

.widget-main {
    min-height: 420px;
}

.widget-search {
    margin-bottom: 24px;
}

.search-input {
    font-size: 1.45em;
    border-style: none;
    padding: 5px 8px;
}

.widget-section {
    border-bottom: 2px solid #ddd;
}

.widget-section h3 {
    font-weight: normal;
}

</style>
