import {
  Client,
  createRestAppClient,
  givenHttpServerConfig,
  expect,
} from '@loopback/testlab';
import {MyCarApplication} from '../..';

describe('PingController', () => {
  let app: MyCarApplication;
  let client: Client;

  before(givenAnApplication);

  before(async () => {
    await app.boot();
    await app.start();
  });

  before(() => {
    client = createRestAppClient(app);
  });

  after(async () => {
    await app.stop();
  });

  it('invokes GET /ping', async () => {
    const res = await client.get('/ping?msg=world').expect(200);
    expect(res.body).to.containEql({greeting: 'Hello from LoopBack'});
  });

  function givenAnApplication() {
    app = new MyCarApplication({
      rest: givenHttpServerConfig(),
    });
  }
});
