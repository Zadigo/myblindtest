<template>
  <section class="site">
    <Navbar>
      <NavbarContent>
        <template #brand>
          <RouterLink :to="{ name: 'home' }">
            Blindtest
          </RouterLink>
        </template>

        <NavbarLinks>
          <NavbarLink>
            <RouterLink :to="{ name: 'blind_test' }">
              Blindtest
            </RouterLink>
          </NavbarLink>

          <NavbarLink>
            <RouterLink :to="{ name: 'create' }">
              Create
            </RouterLink>
          </NavbarLink>
        </NavbarLinks>
      </NavbarContent>
    </Navbar>

    <Toaster position="top-right" />

    <!-- Main -->
    <RouterView />
  </section>
</template>

<script setup lang="ts">
import { Toaster } from 'vue-sonner'
</script>
