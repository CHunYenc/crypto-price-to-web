var app = new Vue({
  el: "#app",
  delimiters: ["[[", "]]"],
  data() {
    return {
      text: "Hello Vue2",
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
    };
  },
  created() {
    var domain = "http://localhost:5000/ws";
    this.socket = io.connect(domain);
    this.socket.on("connect", () => {
      this.select_exchange_disabled = false;
    });
    this.socket.on("get_exchange", (result) => {
      this.select_exchange_items = result;
    });
    this.socket.on("get_symbol", (result) => {
      this.select_symbol_items = result;
      this.select_symbol_disabled = false;
    });
    this.socket.on("get_symbol_data", (result) => {
      this.symbol_data = result;
    });
  },
  methods: {
    select_exchange_method(value) {
      // console.log(value);
      this.socket.emit("get_symbol", { data: this.select_exchange });
    },
    select_data() {
      console.log(
        `select exchange is ${this.select_exchange}, symbol is ${this.select_symbol}.`
      );
      this.socket.emit("get_symbol_data", {
        exchange: this.select_exchange,
        symbol: this.select_symbol,
      });
    },
  },
});
