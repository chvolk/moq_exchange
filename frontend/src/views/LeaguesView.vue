<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-card-title class="text-h4 mb-4">
          My Leagues
          <v-btn
            color="primary"
            class="ml-4"
            @click="showCreateLeagueDialog = true"
          >
            Create League
          </v-btn>
        </v-card-title>
      </v-col>
    </v-row>

    <!-- League Cards -->
    <v-row>
      <v-col
        v-for="league in leagues"
        :key="league.id"
        cols="12"
        md="6"
        lg="4"
      >
        <v-card>
          <v-card-title>{{ league.name }}</v-card-title>
          <v-card-text>
            <div>Type: {{ formatLeagueType(league.league_type) }}</div>
            <div>Members: {{ league.members.length }}/{{ league.max_members }}</div>
            <div>Trades per day: {{ league.trades_per_day }}</div>
            <div>
              Duration: {{ formatDate(league.start_date) }} - {{ formatDate(league.end_date) }}
            </div>
          </v-card-text>
          <v-card-actions>
            <v-btn
              color="primary"
              @click="viewLeague(league.id)"
            >
              View League
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <!-- Create League Dialog -->
    <v-dialog
      v-model="showCreateLeagueDialog"
      max-width="600px"
    >
      <v-card>
        <v-card-title>Create New League</v-card-title>
        <v-card-text>
          <v-form ref="form">
            <v-text-field
              v-model="newLeague.name"
              label="League Name"
              required
            ></v-text-field>

            <v-select
              v-model="newLeague.league_type"
              :items="leagueTypes"
              label="League Type"
              required
            ></v-select>

            <v-row>
              <v-col cols="6">
                <v-menu
                  ref="startMenu"
                  v-model="startMenu"
                  :close-on-content-click="false"
                  transition="scale-transition"
                >
                  <template v-slot:activator="{ props }">
                    <v-text-field
                      v-model="newLeague.start_date"
                      label="Start Date"
                      v-bind="props"
                      readonly
                    ></v-text-field>
                  </template>
                  <v-date-picker
                    v-model="newLeague.start_date"
                    @input="startMenu = false"
                  ></v-date-picker>
                </v-menu>
              </v-col>

              <v-col cols="6">
                <v-menu
                  ref="endMenu"
                  v-model="endMenu"
                  :close-on-content-click="false"
                  transition="scale-transition"
                >
                  <template v-slot:activator="{ props }">
                    <v-text-field
                      v-model="newLeague.end_date"
                      label="End Date"
                      v-bind="props"
                      readonly
                    ></v-text-field>
                  </template>
                  <v-date-picker
                    v-model="newLeague.end_date"
                    @input="endMenu = false"
                  ></v-date-picker>
                </v-menu>
              </v-col>
            </v-row>

            <v-text-field
              v-model="newLeague.trades_per_day"
              label="Trades Per Day"
              type="number"
              required
            ></v-text-field>

            <v-text-field
              v-model="newLeague.max_members"
              label="Maximum Members"
              type="number"
              required
            ></v-text-field>

            <!-- Conditional fields based on league type -->
            <template v-if="newLeague.league_type === 'RANDOM'">
              <v-text-field
                v-model="newLeague.stocks_per_day"
                label="Number of Random Stocks Per Day"
                type="number"
                required
              ></v-text-field>
            </template>

            <template v-if="newLeague.league_type === 'PACK'">
              <v-text-field
                v-model="newLeague.packs_per_player"
                label="Packs Per Player"
                type="number"
                required
              ></v-text-field>
            </template>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="error"
            @click="showCreateLeagueDialog = false"
          >
            Cancel
          </v-btn>
          <v-btn
            color="primary"
            @click="createLeague"
          >
            Create
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

export default {
  name: 'LeaguesView',
  setup() {
    const router = useRouter()
    const leagues = ref([])
    const showCreateLeagueDialog = ref(false)
    const startMenu = ref(false)
    const endMenu = ref(false)

    const leagueTypes = [
      { text: 'Standard League', value: 'STANDARD' },
      { text: 'Random Stocks', value: 'RANDOM' },
      { text: 'Pack Draft', value: 'PACK' },
      { text: 'Chaos League', value: 'CHAOS' }
    ]

    const newLeague = ref({
      name: '',
      league_type: 'STANDARD',
      start_date: '',
      end_date: '',
      trades_per_day: 10,
      max_members: 10,
      stocks_per_day: 0,
      packs_per_player: 0
    })

    const fetchLeagues = async () => {
      try {
        const response = await axios.get('/api/leagues/')
        leagues.value = response.data
      } catch (error) {
        console.error('Error fetching leagues:', error)
      }
    }

    const createLeague = async () => {
      try {
        await axios.post('/api/leagues/', newLeague.value)
        showCreateLeagueDialog.value = false
        await fetchLeagues()
      } catch (error) {
        console.error('Error creating league:', error)
      }
    }

    const viewLeague = (leagueId) => {
      router.push(`/leagues/${leagueId}`)
    }

    const formatDate = (date) => {
      return new Date(date).toLocaleDateString()
    }

    const formatLeagueType = (type) => {
      return leagueTypes.find(t => t.value === type)?.text || type
    }

    onMounted(fetchLeagues)

    return {
      leagues,
      showCreateLeagueDialog,
      startMenu,
      endMenu,
      leagueTypes,
      newLeague,
      createLeague,
      viewLeague,
      formatDate,
      formatLeagueType
    }
  }
}
</script> 