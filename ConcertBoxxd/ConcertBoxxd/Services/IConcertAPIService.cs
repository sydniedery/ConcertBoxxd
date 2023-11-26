using ConcertBoxxd.Data;
using ConcertBoxxd.Services;

namespace ConcertBoxxd.Data
{
    public interface IConcertAPIService
    {

        Task<List<Song_>> GetSetlist(string mbid, int id);
        Task<Concert> GetConcertData(string mbid);


    }
}