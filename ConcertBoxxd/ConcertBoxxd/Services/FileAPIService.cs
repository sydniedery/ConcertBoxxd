using System.Runtime.CompilerServices;
using System.Text;
using System.Text.Json;
using ConcertBoxxd.Data;
using ConcertBoxxd.Services;

namespace Pokemon_Demonstration.Services
{
    public class FileAPIService 
    {

        private HttpClient client;
        protected virtual string BASE_ADDR => "http://localhost:80";


        public FileAPIService()
        {
            client = new HttpClient();
        }

        public async Task<int> ConcertCount()
        {
            var apiCountResponse = await client.GetFromJsonAsync<JsonElement>($"{BASE_ADDR}/Concerts/Count");
            return apiCountResponse.GetInt32();
        }
        public async Task<int> SongCount()
        {
            var apiCountResponse = await client.GetFromJsonAsync<JsonElement>($"{BASE_ADDR}/Songs/Count");
            return apiCountResponse.GetInt32();
        }

        public async Task<Concert> GetConcert(int id)
        {
            var apiResponse = await client.GetFromJsonAsync<JsonElement>($"{BASE_ADDR}/Concerts/{id}");

            return new Concert(id, apiResponse.GetProperty("Mbid").ToString(), apiResponse.GetProperty("Date").ToString(), apiResponse.GetProperty("Artist").ToString(), apiResponse.GetProperty("Tour").ToString(), apiResponse.GetProperty("City").ToString(), apiResponse.GetProperty("State").ToString(), apiResponse.GetProperty("Venue").ToString());
        }

        public async Task PostConcert(Concert concert)
        {
            try
            {
                string json = '{' + $"\"ID\":\"{concert.ID}\",\n" +
                                    $"\"Mbid\":\"{concert.Mbid}\",\n" +
                                    $"\"Date\":\"{concert.Date}\",\n" +
                                    $"\"Artist\":\"{concert.Artist}\",\n" +
                                    $"\"Tour\":\"{concert.Tour}\",\n" +
                                    $"\"City\":\"{concert.City}\",\n" +
                                    $"\"State\":\"{concert.State}\",\n" +
                                    $"\"Venue\":\"{concert.Venue}\"" + '}';

                StringContent JsonContent = new StringContent(json, Encoding.UTF8, "application/json");

                await client.PostAsync($"{BASE_ADDR}/Concerts", JsonContent);
            }
            catch (HttpRequestException ex)
            {
                Console.WriteLine("Failed to post the Conceert. The Concert may already exist. \n" + ex.Message);
            }
        }
        public async Task PostSong(Song_ song)
        {
            try
            {
                string json = '{' + $"\"ID\":\"{song.Id}\",\n" +
                                    $"\"song\":\"{song.Name}\",\n" + '}';

                StringContent JsonContent = new StringContent(json, Encoding.UTF8, "application/json");

                await client.PostAsync($"{BASE_ADDR}/Concerts", JsonContent);
            }
            catch (HttpRequestException ex)
            {
                Console.WriteLine("Failed to post the Conceert. The Concert may already exist. \n" + ex.Message);
            }
        }

        public async Task DeleteConcert(int id)
        {
            await client.DeleteAsync($"{BASE_ADDR}/Concerts/{id}");
        }

        public async Task DeleteSong(int id)
        {
            await client.DeleteAsync($"{BASE_ADDR}/Songs/{id}");
        }
    }
}
