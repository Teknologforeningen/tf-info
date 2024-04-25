export type Env = {
  camUrl: string;
  ylonzDate: Date;
  votesUrl: string;
  pageTimeout: string;
  refreshTime: string;
};

const {
  CAM_URL,
  YLONZ_DATE,
  VOTES_URL,
  PAGE_TIMEOUT = "10s",
  REFRESH_TIME = "04:00",
} = Deno.env.toObject();

export const env: Env = {
  camUrl: CAM_URL,
  ylonzDate: new Date(YLONZ_DATE),
  votesUrl: VOTES_URL,
  pageTimeout: PAGE_TIMEOUT,
  refreshTime: REFRESH_TIME,
};
