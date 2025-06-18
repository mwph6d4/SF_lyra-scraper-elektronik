// src/EventBus.ts
import mitt from "mitt";

type Events = {
  "user-logged-in": void;
  "user-logged-out": void;
};

export const eventBus = mitt<Events>();
