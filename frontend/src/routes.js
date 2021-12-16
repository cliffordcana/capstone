import React from "react";
import { Switch, Route } from "react-router-dom";
import ItemList from "./pages/ItemList";
import PendingOrder from "./pages/PendingOrder";
import ActivityLog from "./pages/ActivityLog";
import Inventory from "./pages/Inventory";
import Transaction from "./pages/Transaction";
import Sales from "./pages/Sales";
import Login from "./pages/Login";

const BaseRouter = () => (
  <Switch>
    <Route exact path="/" component={ItemList} />{" "}
    <Route exact path="/pending-order" component={PendingOrder} />{" "}
    <Route exact path="/activity-log" component={ActivityLog} />{" "}
    <Route exact path="/item/inventory" component={Inventory} />{" "}
    <Route exact path="/transaction" component={Transaction} />{" "}
    <Route exact path="/transaction/sales" component={Sales} />{" "}
    <Route exact path="/login" component={Login} />{" "}
  </Switch>
);

export default BaseRouter;
