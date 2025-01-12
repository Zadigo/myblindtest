<template>
  <nav class="navbar navbar-expand-lg bg-body-light shadow-sm">
    <div class="container-fluid">
      <RouterLink :to="{ name: 'home' }" class="navbar-brand">
        Blind test
      </RouterLink>

      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <FontAwesomeIcon icon="bars" />
      </button>
      
      <div id="navbarNav" class="collapse navbar-collapse">
        <ul class="navbar-nav">
          <li class="nav-item">
            <RouterLink :to="{ name: 'statistics' }" class="nav-link" aria-current="page">
              Statistics
            </RouterLink>
          </li>

          <li class="nav-item">
            <RouterLink :to="{ name: 'create' }" class="nav-link">
              Add songs
            </RouterLink>
          </li>
        </ul>
      </div>
    </div>
  </nav>

  <!-- color="blue-darken-1" -->
  <!-- <v-toolbar :elevation="2">
    <v-app-bar-nav-icon />

    <v-toolbar-title>
      <RouterLink to="/" style="cursor: pointer">
        <span class="fw-bold text-uppercase">
          Blind Test
        </span>
      </RouterLink>
    </v-toolbar-title>

    <RouterLink :to="{ name: 'statistics' }">
      Statistics
    </RouterLink>

    <RouterLink :to="{ name: 'create' }">
      Add songs
    </RouterLink>

    <v-spacer />

    <v-btn icon>
      <v-icon>mdi-export</v-icon>
    </v-btn>
  </v-toolbar> -->
</template>

<script lang="ts" setup>
</script>

<style lang="scss" scoped>
.router-link-exact-active {
  color: rgba($color: #000000, $alpha: 1.0);
}
</style>
