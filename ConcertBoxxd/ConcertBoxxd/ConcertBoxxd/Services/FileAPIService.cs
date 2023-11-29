using System;
using System.Runtime.CompilerServices;
using System.Text;
using System.Text.Json;
using ConcertBoxxd.Data;
using ConcertBoxxd.Services;
using Newtonsoft.Json;

namespace ConcertBoxxd.Services
{

    public class FileAPIService
    {

        private HttpClient client;
        protected virtual string BASE_ADDR => "http://localhost:8000";


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

        public async Task<List<Song>> GetSetlist(int concertID)
        {
            try
            {
                var response = await client.GetStringAsync($"{BASE_ADDR}/Concerts/Songs/{concertID}");

                var apiResponse = JsonConvert.DeserializeObject<List<Song>>(response);


                if (apiResponse != null)
                {
                    //working on this. delete whole method if needed
                    return apiResponse;
                }
                else
                {
                    // Handle the case when the API response is not in the expected format
                    return new List<Song>();
                }
            }
            catch (Exception ex)
            {
                // Handle exceptions (e.g., network issues, JSON deserialization errors)
                Console.WriteLine($"Error: {ex.Message}");
                throw;
            }
        }



        public async Task PostConcert(Concert concert)
        {
            try
            {
                string json = '{' + $"\"ID\":{concert.ID},\n" +
                                    $"\"Mbid\":\"{concert.Mbid}\",\n" +
                                    $"\"Date\":\"{concert.Date}\",\n" +
                                    $"\"Artist\":\"{concert.Artist}\",\n" +
                                    $"\"Tour\":\"{concert.Tour}\",\n" +
                                    $"\"City\":\"{concert.City}\",\n" +
                                    $"\"State\":\"{concert.State}\",\n" +
                                    $"\"Venue\":\"{concert.Venue}\"" + '}';

                StringContent JsonContent = new StringContent(json, Encoding.UTF8, "application/json");
                Console.Write(json);
                await client.PostAsync($"{BASE_ADDR}/Concerts", JsonContent);
            }
            catch (HttpRequestException ex)
            {
                Console.WriteLine("Failed to post the Conceert. The Concert may already exist. \n" + ex.Message);
            }
        }
        public async Task PostSong(Song song)
        {
            try
            {
                string json = '{' + $"\"ID\":\"{song.ID}\",\n" +
                                    $"\"song\":\"{song.Name}\",\n" + '}';

                StringContent JsonContent = new StringContent(json, Encoding.UTF8, "application/json");

                await client.PostAsync($"{BASE_ADDR}/Songs", JsonContent);
            }
            catch (HttpRequestException ex)
            {
                Console.WriteLine("Failed to post the Conceert. The Concert may already exist. \n" + ex.Message);
            }
        }

        public async Task PostConcertSong (Concert concert, Song song)
        {
            try
            {
                string json = '{' + $"\"Concert_ID\":\"{concert.ID}\",\n" +
                                    $"\"SongID\":\"{song.ID}\",\n" + '}';

                StringContent JsonContent = new StringContent(json, Encoding.UTF8, "application/json");

                await client.PostAsync($"{BASE_ADDR}/Songs", JsonContent);
            }
            catch (HttpRequestException ex)
            {
                Console.WriteLine("Failed to post the Song to the Concert. The Song may already exist. \n" + ex.Message);
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
