using ConcertBoxxd.Data;
using System.Net.Http.Headers;
using System.Text.Json;
using System;
using Newtonsoft.Json;
using System.Net.Http;

namespace ConcertBoxxd.Services
{
    public class Country
    {
        public string Code { get; set; }
        public string Name { get; set; }
    }

    public class City
    {
        public string Name { get; set; }
        public string StateCode { get; set; }
        public Country Country { get; set; }
    }

    public class Artist
    {
        public string Mbid { get; set; }
        public string Name { get; set; }
    }

    public class Venue
    {
        public string Name { get; set; }
        public City City { get; set; }
    }

    public class Song
    {
        public string Name { get; set; }
        public Cover Cover { get; set; }
        public string Info { get; set; }
    }

    public class Cover
    {
        public string Mbid { get; set; }
        public string Name { get; set; }
    }

    public class Set
    {
        public int Encore { get; set; }
        public Song[] Song { get; set; }
    }

    public class Sets
    {
        public Set[] Set { get; set; }
    }

    public class Tour
    {
        public string Name { get; set; }
    }

    public class Root
    {
        public string Id { get; set; }
        public string EventDate { get; set; }
        public Artist Artist { get; set; }
        public Venue Venue { get; set; }
        public Tour Tour { get; set; }
        public Sets Sets { get; set; }
        public string Info { get; set; }
    }
    public class ConcertAPIService : IConcertAPIService
    {
        private HttpClient client;

        public ConcertAPIService()
        {
            client = new HttpClient();
            client.BaseAddress = new Uri($"https://api.setlist.fm/rest/1.0/setlist/3ba10c34");
            client.DefaultRequestHeaders.Accept.Clear();
            client.DefaultRequestHeaders.Add("X-Api-Key", "lFMgUHCUEzzdvwIV6lCbO4bAxzZdPwUlzHrA");
            client.DefaultRequestHeaders.Accept.Add(
               new MediaTypeWithQualityHeaderValue("application/json"));
        }

        public async Task<Concert> GetConcertData(string mbid)
        {
            var apiResponse = await client.GetFromJsonAsync<JsonElement>($"https://api.setlist.fm/rest/1.0/setlist/{mbid}");
            // Deserialize the JSON into a C# object
            Root deserializedData = JsonConvert.DeserializeObject<Root>(apiResponse.ToString());
           Concert concert = new Concert(deserializedData.Id, deserializedData.EventDate, deserializedData.Artist.Name, deserializedData.Tour.Name, deserializedData.Venue.City.Name, deserializedData.Venue.City.StateCode, deserializedData.Venue.Name);
            return concert;
        }

        public async Task<List<Song_>> GetSetlist(string mbid, int id)
        {
            List<Song_> setlist = new List<Song_>();

            var apiResponse = await client.GetFromJsonAsync<JsonElement>($"https://api.setlist.fm/rest/1.0/setlist/{mbid}");
            // Deserialize the JSON into a C# object
            Root deserializedData = JsonConvert.DeserializeObject<Root>(apiResponse.ToString());
            foreach (var set in deserializedData.Sets.Set)
            { 
                foreach(var song in set.Song)
                {
                    setlist.Add(new Song_(id, song.Name));

                }
            }


            return setlist;
        }

    }
}