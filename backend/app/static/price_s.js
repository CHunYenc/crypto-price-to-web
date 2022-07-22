var app = new Vue({
  el: '#app',
  delimiters: ['[[', ']]'],
  data() {
    return {
      text: 'Hello Vue2',
      socket: null,
      // select exchange
      select_exchange_items: [],
      select_exchange: null,
      select_exchange_loading: true,
      select_exchange_disabled: true,
      // select symbol
      select_symbol_items: [],
      select_symbol: null,
      select_symbol_loading: true,
      select_symbol_disabled: true,
      // exchange and symbol data
      symbol_data: {},
      current_price: null
    }
  },
  created() {
    var domain = `ws://${window.location.hostname}:${window.location.port}/ws`
    // console.log(domain);
    this.socket = io.connect(domain)
    this.socket.on('connect', () => {
      this.select_exchange_disabled = false
    })
    this.socket.on('get_exchange', (result) => {
      this.select_exchange_items = result
    })
    this.socket.on('get_symbol', (result) => {
      this.select_symbol_items = result
      this.select_symbol_disabled = false
    })
    this.socket.on('get_symbol_data', (result) => {
      console.log('get_symbol_data')
      this.symbol_data = result
      if (this.select_exchange.includes('BINANCE')) {
        this.current_price = this.symbol_data.info.lastPrice
      }
      document.title = `${this.current_price} - ${this.select_exchange} - ${this.select_symbol}`
    })
  },
  methods: {
    select_exchange_method(value) {
      // console.log(value);
      this.socket.emit('get_symbol', { data: this.select_exchange })
    },
    select_data() {
      console.log(
        `select exchange is ${this.select_exchange}, symbol is ${this.select_symbol}.`
      )
      this.socket.emit('get_symbol_data', {
        exchange: this.select_exchange,
        symbol: this.select_symbol
      })
    }
  }
})
