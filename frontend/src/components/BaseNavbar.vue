<template>
  <Navbar>
    <NavbarContent>
      Something
    </NavbarContent>
  </Navbar>

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
