<template>
  <section class="w-5xl mx-auto px-10 relative">
    <Card class="mt-10 mb-5">
      <CardContent>
        <Button class="ml-auto rounded-full" as-child>
          <RouterLink :to="{ name: 'teams' }">
            Manage teams
            <VueIcon icon="fa-solid:arrow-right" />
          </RouterLink>
        </Button>
      </CardContent>
    </Card>

    <div class="grid grid-cols-2 gap-2">
      <GeneralSettings />
      <PointValues />
      <GameModes />
    </div>
  </section>
</template>

<script lang="ts" setup>
import type { GenreDistribution, SettingsDataApiResponse } from '@/types'
import { toast } from 'vue-sonner'

const { client } = useAxiosClient()
const songStore = useSongs()

// TODO: Place in cache
const minimumPeriod = ref<number>(0)
const maximumPeriod = ref<number>(100)
const genreDistribution = ref<GenreDistribution[]>([])

/**
 *
 */
async function requestSettingsData() {
  try {
    const response = await client.get<SettingsDataApiResponse>('/api/v1/songs/settings')

    songStore.cache.settings.timeRange[0] = response.data.period.minimum
    songStore.cache.settings.timeRange[1] = response.data.period.maximum

    minimumPeriod.value = response.data.period.minimum
    maximumPeriod.value = response.data.period.maximum

    genreDistribution.value = response.data.count_by_genre
  } catch {
    toast.error('Could not get settings')
  }
}

onBeforeMount(requestSettingsData)
</script>

<style lang="scss">
#side-panel {
  #panel {
    position: sticky;
    top: 0;
    left: 0;
  }
}
</style>
