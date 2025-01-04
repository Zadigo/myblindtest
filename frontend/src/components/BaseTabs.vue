<template>
  <ul class="nav nav-pills">
    <li class="nav-item">
      <RouterLink :to="{ name: 'blind_test' }" class="nav-link" aria-current="page">
        Blind test
      </RouterLink>
    </li>
    
    <li class="nav-item">
      <RouterLink :to="{ name: 'settings' }" class="nav-link">
        <FontAwesomeIcon class="me-2" icon="cog" />
        Settings
      </RouterLink>
    </li>
  </ul>
</template>

<script setup lang="ts">
</script>

<style lang="scss" scoped>
.router-link-exact-active {
  background-color: rgba($color: #e2eaf7, $alpha: 1.0);
}
</style>
