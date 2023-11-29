using ConcertBoxxd.Data;
using ConcertBoxxd.Services;

namespace ConcertBoxxd.Data
{
    public interface IConcertAPIService
    {
        Task<int> ConcertCount();
        Task<int> SongCount();

        //Task<List<Song>> GetSetlist(string mbid, int id);
      //  Task<Concert> GetConcertData(string mbid, int id);


    }
}