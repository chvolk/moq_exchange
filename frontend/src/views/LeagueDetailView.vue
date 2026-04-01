<template>
  <v-container>
    <v-overlay :model-value="loading" class="align-center justify-center">
      <v-progress-circular
        color="primary"
        indeterminate
        size="64"
      ></v-progress-circular>
    </v-overlay>
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title class="text-h4">
            {{ league.name }}
          </v-card-title>
          <v-card-text>
            <v-row>
              <v-col cols="12" md="6">
                <div class="text-h6">League Info</div>
                <div>Type: {{ formatLeagueType(league.league_type) }}</div>
                <div>Trades Today: {{ portfolio.trades_today }}/{{ league.trades_per_day }}</div>
                <div>Balance: ${{ formatMoney(portfolio.balance) }}</div>
                <div>Total Value: ${{ formatMoney(portfolio.total_value) }}</div>
                <div>Gain/Loss: ${{ formatMoney(portfolio.total_gain_loss) }}</div>
              </v-col>
              <v-col cols="12" md="6">
                <div class="text-h6">Leaderboard</div>
                <v-list>
                  <v-list-item
                    v-for="(player, index) in leaderboard"
                    :key="player.user"
                  >
                    <template v-slot:prepend>
                      {{ index + 1 }}.
                    </template>
                    <v-list-item-title>
                      {{ player.username }}
                    </v-list-item-title>
                    <v-list-item-subtitle>
                      ${{ formatMoney(player.total_value) }}
                    </v-list-item-subtitle>
                  </v-list-item>
                </v-list>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Portfolio Section -->
    <v-row class="mt-4">
      <v-col cols="12">
        <v-card>
          <v-card-title>My Portfolio</v-card-title>
          <v-card-text>
            <v-data-table
              :headers="headers"
              :items="portfolioStocks"
              :items-per-page="10"
            >
              <template v-slot:item.actions="{ item }">
                <v-btn
                  color="error"
                  size="small"
                  @click="sellStock(item)"
                  :disabled="!canTrade"
                >
                  Sell
                </v-btn>
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Trading Section -->
    <v-row class="mt-4">
      <v-col cols="12">
        <v-card>
          <v-card-title>
            Available Stocks
            <v-spacer></v-spacer>
            <v-text-field
              v-model="search"
              append-icon="mdi-magnify"
              label="Search"
              single-line
              hide-details
            ></v-text-field>
          </v-card-title>
          <v-card-text>
            <v-data-table
              :headers="availableStockHeaders"
              :items="availableStocks"
              :items-per-page="10"
              :search="search"
            >
              <template v-slot:item.actions="{ item }">
                <v-btn
                  color="primary"
                  size="small"
                  @click="buyStock(item)"
                  :disabled="!canTrade"
                >
                  Buy
                </v-btn>
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Buy Stock Dialog -->
    <v-dialog v-model="buyDialog" max-width="400px">
      <v-card>
        <v-card-title>Buy Stock</v-card-title>
        <v-card-text>
          <v-row>
            <v-col cols="12">
              <div>Symbol: {{ selectedStock?.symbol }}</div>
              <div>Current Price: ${{ formatMoney(selectedStock?.current_price) }}</div>
              <v-text-field
                v-model="quantity"
                label="Quantity"
                type="number"
                min="1"
                :max="Math.floor(leaguePortfolio?.balance / selectedStock?.current_price)"
              ></v-text-field>
              <div>Total Cost: ${{ formatMoney(selectedStock?.current_price * quantity) }}</div>
            </v-col>
          </v-row>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="error" @click="buyDialog = false">Cancel</v-btn>
          <v-btn color="primary" @click="confirmBuy" :loading="loading">Buy</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Sell Stock Dialog -->
    <v-dialog v-model="sellDialog" max-width="400px">
      <v-card>
        <v-card-title>Sell Stock</v-card-title>
        <v-card-text>
          <v-row>
            <v-col cols="12">
              <div>Symbol: {{ selectedStock?.stock?.symbol }}</div>
              <div>Current Price: ${{ formatMoney(selectedStock?.stock?.current_price) }}</div>
              <v-text-field
                v-model="quantity"
                label="Quantity"
                type="number"
                min="1"
                :max="selectedStock?.quantity"
              ></v-text-field>
              <div>Total Value: ${{ formatMoney(selectedStock?.stock?.current_price * quantity) }}</div>
            </v-col>
          </v-row>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="error" @click="sellDialog = false">Cancel</v-btn>
          <v-btn color="primary" @click="confirmSell" :loading="loading">Sell</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Error Snackbar -->
    <v-snackbar v-model="showError" color="error" timeout="3000">
      {{ error }}
      <template v-slot:actions>
        <v-btn variant="text" @click="showError = false">Close</v-btn>
      </template>
    </v-snackbar>
  </v-container>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { useLeagueStore } from '@/stores/leagueStore'
import { storeToRefs } from 'pinia'

export default {
  name: 'LeagueDetailView',
  setup() {
    const route = useRoute()
    const leagueStore = useLeagueStore()
    const search = ref('')
    // Add these new refs
    const showError = ref(false)
    const buyDialog = ref(false)
    const sellDialog = ref(false)
    const selectedStock = ref(null)
    const quantity = ref(1)

    // ... existing store refs and other setup code ...

    // Add these new methods
    const confirmBuy = async () => {
      try {
        loading.value = true
        await axios.post(`/api/leagues/${route.params.id}/trade/`, {
          symbol: selectedStock.value.symbol,
          quantity: quantity.value,
          action: 'buy'
        })
        buyDialog.value = false
        await refreshData()
      } catch (err) {
        error.value = err.response?.data?.error || 'Failed to buy stock'
        showError.value = true
      } finally {
        loading.value = false
      }
    }

    const confirmSell = async () => {
      try {
        loading.value = true
        await axios.post(`/api/leagues/${route.params.id}/trade/`, {
          symbol: selectedStock.value.stock.symbol,
          quantity: quantity.value,
          action: 'sell'
        })
        sellDialog.value = false
        await refreshData()
      } catch (err) {
        error.value = err.response?.data?.error || 'Failed to sell stock'
        showError.value = true
      } finally {
        loading.value = false
      }
    }

    return {
      // ... existing returns ...
      showError,
      buyDialog,
      sellDialog,
      confirmBuy,
      confirmSell,
      selectedStock,
      quantity
    }
  }
}
</script>
