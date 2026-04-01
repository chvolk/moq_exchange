<template>
  <v-container fluid class="fill-height pa-0" style="background: linear-gradient(to right, #2196F3, #4CAF50);">
    <v-row align="center" justify="center" class="mx-0">
      <v-col cols="12" md="10" lg="8">
        <v-card elevation="12" class="pa-6">
          <v-card-title class="text-center mb-6">
            <h1 class="display-2 font-weight-bold leaderboard-title">
              <span class="title-word title-word-3">Leaderboard</span>
            </h1>
          </v-card-title>

          <v-tabs v-model="activeTab" centered>
            <v-tab class="weekly_tab">Weekly Portfolio Value</v-tab>
            <v-tab class="moq_tab">Total Moqs</v-tab>
          </v-tabs>

          <v-window v-model="activeTab">
            <v-window-item>
              <v-data-table
                :headers="headers"
                :items="filteredLeaderboard"
                :items-per-page="10"
                class="elevation-1"
              >
                <template v-slot:item.gain_loss="{ item }">
                  <span :class="item.gain_loss >= 0 ? 'success--text' : 'error--text'">
                    {{ item.gain_loss >= 0 ? '+' : '-' }}${{ Math.abs(item.gain_loss).toFixed(2) }}
                  </span>
                </template>
              </v-data-table>
            </v-window-item>

            <v-window-item>
              <v-data-table
                :headers="moqHeaders"
                :items="filteredMoqLeaderboard"
                :items-per-page="10"
                class="elevation-1"
              >
              </v-data-table>
            </v-window-item>
          </v-window>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>
  
  <script>
  import axios from 'axios'
  import { VTabs, VTab } from 'vuetify/components'
  export default {
    name: 'Leaderboard',
    components: {
      VTabs,
      VTab
    },
    
    data: () => ({
      activeTab: 0,
      headers: [
        { title: 'Rank', align: 'start', value: 'rank' },
        { title: 'Username', align: 'start', value: 'username' },
        { title: 'Total Value', align: 'end', value: 'total_value' },
        { title: 'Gain/Loss', align: 'end', value: 'gain_loss' },
      ],
      leaderboard: [],
      moqHeaders: [
      { title: 'Rank', align: 'start', value: 'rank' },
      { title: 'Username', align: 'start', value: 'username' },
      { title: 'Total Moqs', align: 'end', value: 'total_moqs' },
      ],
      moqLeaderboard: [],
    }),
    mounted() {
      this.fetchLeaderboard()
      this.fetchMoqLeaderboard()
    },
    computed: {
      filteredLeaderboard() {
        // return this.leaderboard.filter(item => Number(item.total_value) !== 50000.00 )
        return this.leaderboard
      },
      filteredMoqLeaderboard() {
        return this.moqLeaderboard.filter(item => Number(item.total_moqs) !== 600)
      }
    },
    methods: {
      async fetchLeaderboard() {
        try {
          const token = localStorage.getItem('token')
          const response = await axios.get('/api/leaderboard/', {
            headers: {
              'Authorization': `Token ${token}`
            }
          })
          this.leaderboard = response.data.map((item, index) => ({
            ...item,
            rank: index + 1,
            total_value: Number(item.total_value).toFixed(2),
            gain_loss: Number(item.gain_loss)
          }))
        } catch (error) {
          console.error('Error fetching leaderboard:', error)
        }
      },
      async fetchMoqLeaderboard() {
        try {
          const token = localStorage.getItem('token')
          const response = await axios.get('/api/moq-leaderboard/', {
            headers: {
              'Authorization': `Token ${token}`
            }
          })
          console.log(response)
          this.moqLeaderboard = response.data.map((item, index) => ({
            ...item,
            rank: index + 1,
            total_moqs: Number(item.total_moqs).toFixed(2),
          }))
          console.log(this.moqLeaderboard)
        } catch (error) {
          console.error('Error fetching moq leaderboard:', error)
        }
      }
    }
  }
  </script>
  
  <style scoped>
  .success--text {
    color: #4CAF50 !important;
  }
  
  .error--text {
    color: #F44336 !important;
  }
  .weekly_tab {
    background-color: #d60cff;
    color: #ffffff;
  }
  .moq_tab {
    background-color: #2dca6f;
    color: #ffffff;
  }
  .leaderboard-title {
    background: linear-gradient(to right, #30CFD0 0%, #330867 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 3rem;
    text-transform: uppercase;
    letter-spacing: 2px;
  }
  .title-word {
    animation: color-animation 4s linear infinite;
  }
  .title-word-3 {
    --color-1: #ACCFCB;
    --color-2: #E4A9A8;
    --color-3: #ACCFCB;
  }
  @keyframes color-animation {
    0%    {color: var(--color-1)}
    32%   {color: var(--color-1)}
    33%   {color: var(--color-2)}
    65%   {color: var(--color-2)}
    66%   {color: var(--color-3)}
    99%   {color: var(--color-3)}
    100%  {color: var(--color-1)}
  }
  </style>