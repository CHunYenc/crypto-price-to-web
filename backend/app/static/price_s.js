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
      // select symbol
      select_symbol_items: [],
      select_symbol: null,
      select_symbol_loading: true,
    };
  },
  created() {
    var domain = "http://localhost:5000/ws";
    this.socket = io.connect(domain);
    this.socket.on("connect", () => {});
    this.socket.on("get_exchange", (result) => {
      this.select_exchange_items = result;
    });
    this.socket.on("get_symbol", (result)=>{
        this.select_symbol_items = result
    })
  },
  methods: {
    select_exchange_method(value) {
      // console.log(value);
      this.socket.emit(
        "get_symbol",
        { data: this.select_exchange }
      );
    },
  },
});
